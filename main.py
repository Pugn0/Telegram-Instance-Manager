from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import shutil
import subprocess
import webbrowser
import socket
import psutil
from datetime import datetime
from pathlib import Path
import threading
import time

app = FastAPI(title="Telegram Instance Manager")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminhos
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
WEB_DIR = BASE_DIR / "web"
INSTANCES_FILE = DATA_DIR / "instances.json"

TELEGRAM_BASE = Path(r"C:\Users\pugno\AppData\Roaming\Telegram Desktop")
INSTANCES_BASE = Path(r"C:\Users\pugno\AppData\Roaming\Telegram_Instances")

# Criar diretórios necessários
DATA_DIR.mkdir(exist_ok=True)
INSTANCES_BASE.mkdir(exist_ok=True)

# Models
class InstanceCreate(BaseModel):
    name: str

class InstanceUpdate(BaseModel):
    name: str

# Funções auxiliares
def find_free_port(start_port=8080, max_attempts=100):
    """Encontra uma porta disponível a partir de start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:
                return port
        except:
            continue
    
    raise Exception(f"Nenhuma porta disponível entre {start_port} e {start_port + max_attempts}")

def is_telegram_running(instance_folder):
    """Verifica se o Telegram desta instância está rodando"""
    instance_folder = str(instance_folder)
    
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['name'] and 'telegram' in proc.info['name'].lower():
                if proc.info['exe'] and instance_folder.lower() in proc.info['exe'].lower():
                    return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return False, None

def load_instances():
    """Carrega instâncias do arquivo JSON"""
    if not INSTANCES_FILE.exists():
        return []
    try:
        with open(INSTANCES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar instances.json: {e}")
        return []

def save_instances(instances):
    """Salva instâncias no arquivo JSON"""
    try:
        with open(INSTANCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(instances, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Erro ao salvar instances.json: {e}")
        raise HTTPException(status_code=500, detail="Erro ao salvar dados")

def get_next_id(instances):
    """Retorna o próximo ID disponível"""
    if not instances:
        return 1
    return max(inst['id'] for inst in instances) + 1

def open_browser(url):
    """Abre o navegador após 1.5 segundos"""
    time.sleep(1.5)
    webbrowser.open(url)

# Endpoints
@app.get("/health")
def health_check():
    """Verifica status da API"""
    return {
        "status": "ok",
        "telegram_base_exists": TELEGRAM_BASE.exists(),
        "instances_folder_exists": INSTANCES_BASE.exists()
    }

@app.get("/instances")
def list_instances():
    """Lista todas as instâncias com status de execução"""
    instances = load_instances()
    
    for inst in instances:
        inst['folder_exists'] = Path(inst['folder']).exists()
        inst['telegram_exe_exists'] = (Path(inst['folder']) / "Telegram.exe").exists()
        
        # Verificar se está rodando
        is_running, pid = is_telegram_running(inst['folder'])
        inst['is_running'] = is_running
        inst['pid'] = pid
    
    return instances

@app.post("/instances")
def create_instance(data: InstanceCreate):
    """Cria uma nova instância do Telegram"""
    if not TELEGRAM_BASE.exists():
        raise HTTPException(
            status_code=404, 
            detail=f"Pasta base do Telegram não encontrada: {TELEGRAM_BASE}"
        )
    
    instances = load_instances()
    new_id = get_next_id(instances)
    
    instance_folder = INSTANCES_BASE / f"instance_{new_id}"
    
    try:
        print(f"📦 Criando instância #{new_id}: {data.name}")
        
        shutil.copytree(TELEGRAM_BASE, instance_folder)
        
        new_instance = {
            "id": new_id,
            "name": data.name,
            "folder": str(instance_folder),
            "created_at": datetime.now().isoformat(),
            "last_session": None,
            "folder_exists": True,
            "telegram_exe_exists": True
        }
        
        instances.append(new_instance)
        save_instances(instances)
        
        print(f"✅ Instância #{new_id} criada!")
        return new_instance
        
    except Exception as e:
        if instance_folder.exists():
            shutil.rmtree(instance_folder, ignore_errors=True)
        print(f"❌ Erro ao criar instância: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar instância: {str(e)}")

@app.put("/instances/{instance_id}")
def update_instance(instance_id: int, data: InstanceUpdate):
    """Renomeia uma instância"""
    instances = load_instances()
    
    for inst in instances:
        if inst['id'] == instance_id:
            old_name = inst['name']
            inst['name'] = data.name
            save_instances(instances)
            print(f"✏️ #{instance_id}: {old_name} → {data.name}")
            return inst
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

@app.delete("/instances/{instance_id}")
def delete_instance(instance_id: int):
    """Exclui uma instância"""
    instances = load_instances()
    
    for i, inst in enumerate(instances):
        if inst['id'] == instance_id:
            folder = Path(inst['folder'])
            
            # Verificar se está rodando e encerrar
            is_running, pid = is_telegram_running(folder)
            if is_running and pid:
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    proc.wait(timeout=5)
                except:
                    pass
            
            try:
                if folder.exists():
                    print(f"🗑️ Excluindo #{instance_id}: {inst['name']}")
                    shutil.rmtree(folder)
                
                instances.pop(i)
                save_instances(instances)
                
                print(f"✅ Instância #{instance_id} excluída!")
                return {"message": "Instância excluída com sucesso"}
                
            except Exception as e:
                print(f"❌ Erro ao excluir: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro ao excluir instância: {str(e)}"
                )
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

@app.post("/instances/{instance_id}/start")
def start_instance(instance_id: int):
    """Inicia o Telegram de uma instância"""
    instances = load_instances()
    
    for inst in instances:
        if inst['id'] == instance_id:
            exe_path = Path(inst['folder']) / "Telegram.exe"
            
            if not exe_path.exists():
                raise HTTPException(
                    status_code=404, 
                    detail=f"Telegram.exe não encontrado em: {exe_path}"
                )
            
            # Verificar se já está rodando
            is_running, _ = is_telegram_running(inst['folder'])
            if is_running:
                return {"message": f"Telegram já está em execução: {inst['name']}"}
            
            try:
                print(f"🚀 Iniciando #{instance_id}: {inst['name']}")
                
                subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))
                
                # Atualizar última sessão
                inst['last_session'] = datetime.now().isoformat()
                save_instances(instances)
                
                return {"message": f"Telegram iniciado: {inst['name']}"}
                
            except Exception as e:
                print(f"❌ Erro ao iniciar: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro ao iniciar Telegram: {str(e)}"
                )
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

@app.post("/instances/{instance_id}/stop")
def stop_instance(instance_id: int):
    """Para o Telegram de uma instância"""
    instances = load_instances()
    
    for inst in instances:
        if inst['id'] == instance_id:
            is_running, pid = is_telegram_running(inst['folder'])
            
            if not is_running:
                raise HTTPException(
                    status_code=400, 
                    detail="Telegram não está em execução"
                )
            
            try:
                print(f"🛑 Parando #{instance_id}: {inst['name']}")
                
                proc = psutil.Process(pid)
                proc.terminate()
                
                # Aguardar encerramento
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    proc.kill()
                
                # Atualizar última sessão
                inst['last_session'] = datetime.now().isoformat()
                save_instances(instances)
                
                return {"message": f"Telegram parado: {inst['name']}"}
                
            except Exception as e:
                print(f"❌ Erro ao parar: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro ao parar Telegram: {str(e)}"
                )
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

@app.post("/instances/{instance_id}/open-folder")
def open_folder(instance_id: int):
    """Abre a pasta da instância no Explorer"""
    instances = load_instances()
    
    for inst in instances:
        if inst['id'] == instance_id:
            folder = Path(inst['folder'])
            
            if not folder.exists():
                raise HTTPException(status_code=404, detail="Pasta não encontrada")
            
            try:
                os.startfile(folder)
                return {"message": "Pasta aberta no Explorer"}
            except Exception as e:
                print(f"❌ Erro ao abrir pasta: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro ao abrir pasta: {str(e)}"
                )
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

# Servir favicon
@app.get("/logo.ico")
def serve_favicon():
    """Serve o favicon"""
    favicon_path = BASE_DIR / "logo.ico"
    if favicon_path.exists():
        return FileResponse(favicon_path)
    raise HTTPException(status_code=404, detail="Favicon não encontrado")

# Servir frontend
@app.get("/")
def serve_frontend():
    """Serve a página HTML"""
    html_file = WEB_DIR / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    raise HTTPException(status_code=404, detail="Frontend não encontrado")

if __name__ == "__main__":
    import uvicorn
    import logging
    
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    try:
        port = find_free_port(8080)
        url = f"http://localhost:{port}"
        
        print("=" * 60)
        print("🚀 TELEGRAM INSTANCE MANAGER")
        print("=" * 60)
        print(f"🌐 Servidor: {url}")
        print(f"📊 API Docs: {url}/docs")
        print(f"🔌 Porta: {port}")
        print(f"📁 Pasta base: {TELEGRAM_BASE}")
        print(f"📁 Instâncias: {INSTANCES_BASE}")
        print("=" * 60)
        print("⏳ Abrindo navegador em 1.5s...")
        print("💡 Pressione CTRL+C para parar o servidor")
        print("=" * 60)
        
        threading.Thread(target=open_browser, args=(url,), daemon=True).start()
        
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="warning",
            access_log=False
        )
        
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado!")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        input("Pressione Enter para sair...")