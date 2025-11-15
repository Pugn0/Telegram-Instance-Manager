from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

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
    """Lista todas as instâncias"""
    instances = load_instances()
    print(f"📋 Listando {len(instances)} instâncias")
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
    
    # Criar pasta da nova instância
    instance_folder = INSTANCES_BASE / f"instance_{new_id}"
    
    try:
        print(f"📦 Criando instância {new_id}: {data.name}")
        print(f"   Copiando de: {TELEGRAM_BASE}")
        print(f"   Para: {instance_folder}")
        
        # Copiar pasta base
        shutil.copytree(TELEGRAM_BASE, instance_folder)
        
        # Criar registro da instância
        new_instance = {
            "id": new_id,
            "name": data.name,
            "folder": str(instance_folder),
            "created_at": datetime.now().isoformat()
        }
        
        instances.append(new_instance)
        save_instances(instances)
        
        print(f"✅ Instância {new_id} criada com sucesso!")
        return new_instance
        
    except Exception as e:
        # Limpar pasta se houver erro
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
            print(f"✏️ Instância {instance_id} renomeada: {old_name} → {data.name}")
            return inst
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

@app.delete("/instances/{instance_id}")
def delete_instance(instance_id: int):
    """Exclui uma instância"""
    instances = load_instances()
    
    for i, inst in enumerate(instances):
        if inst['id'] == instance_id:
            folder = Path(inst['folder'])
            
            try:
                # Remover pasta
                if folder.exists():
                    print(f"🗑️ Removendo pasta: {folder}")
                    shutil.rmtree(folder)
                
                # Remover do JSON
                instances.pop(i)
                save_instances(instances)
                
                print(f"✅ Instância {instance_id} excluída com sucesso!")
                return {"message": "Instância excluída com sucesso"}
                
            except Exception as e:
                print(f"❌ Erro ao excluir instância: {e}")
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
            
            try:
                print(f"🚀 Iniciando Telegram da instância {instance_id}: {inst['name']}")
                print(f"   Executando: {exe_path}")
                
                # Iniciar processo
                subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))
                
                print(f"✅ Telegram iniciado com sucesso!")
                return {"message": f"Telegram iniciado: {inst['name']}"}
                
            except Exception as e:
                print(f"❌ Erro ao iniciar Telegram: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro ao iniciar Telegram: {str(e)}"
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
                print(f"📂 Abrindo pasta: {folder}")
                os.startfile(folder)
                return {"message": "Pasta aberta no Explorer"}
            except Exception as e:
                print(f"❌ Erro ao abrir pasta: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Erro ao abrir pasta: {str(e)}"
                )
    
    raise HTTPException(status_code=404, detail="Instância não encontrada")

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
    print("=" * 60)
    print("🚀 TELEGRAM INSTANCE MANAGER")
    print("=" * 60)
    print(f"📍 Servidor: http://localhost:8080")
    print(f"📊 API Docs: http://localhost:8080/docs")
    print(f"📁 Pasta base: {TELEGRAM_BASE}")
    print(f"📁 Instâncias: {INSTANCES_BASE}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8080)