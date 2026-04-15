"""
Antigravity IDE için Özel OpenAI MCP Sunucusu
Bu sunucu, GPT-4o modelini IDE içinden bir araç (tool) olarak kullanmanızı sağlar.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI

# .env dosyasından API anahtarını yükle
load_dotenv()

# OpenAI istemcisini başlat
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# MCP Sunucusunu oluştur
mcp = FastMCP(
    "OpenAI-Custom-Server",
    instructions="Bu sunucu GPT-4o modeline doğrudan erişim sağlar. Kod analizi ve genel sorular için kullanabilirsiniz."
)

@mcp.tool()
def ask_gpt4o(prompt: str, system_message: str = "Sen yetkili bir yazılım asistanısın.") -> str:
    """
    GPT-4o modeline bir soru sorar ve yanıt döner.
    
    Args:
        prompt: Modele gönderilecek ana mesaj veya soru.
        system_message: Modelin davranışını belirleyen sistem mesajı.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

@mcp.tool()
def analyze_code_with_gpt4o(file_path: str, context: Optional[str] = None) -> str:
    """
    Belirtilen bir kod dosyasını okur ve GPT-4o ile analiz eder.
    
    Args:
        file_path: Analiz edilecek dosyanın tam yolu.
        context: Analiz için ekstra bağlam veya odaklanılması gereken nokta.
    """
    if not os.path.exists(file_path):
        return f"Hata: Dosya bulunamadı: {file_path}"
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        
        prompt = f"Aşağıdaki kodu analiz et. {f'Bağlam: {context}' if context else ''}\n\nKod:\n```\n{code_content}\n```"
        
        return ask_gpt4o(prompt, system_message="Sen bir kod analizi uzmanısın. Hataları bul, iyileştirmeler öner ve temiz kod prensiplerine göre değerlendir.")
    except Exception as e:
        return f"Dosya işleme hatası: {str(e)}"

if __name__ == "__main__":
    # Sunucuyu başlat
    mcp.run()
