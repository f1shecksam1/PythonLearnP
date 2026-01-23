# src/learnpyapp/core/config.py
# 🧩 Ortam (environment) değişkenlerinden gelen yapılandırma yönetimi.
# Pydantic Settings, .env dosyasını otomatik okuyarak tip güvenliği sağlar.

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    🔒 BaseSettings, .env dosyasındaki değişkenleri otomatik olarak okur.
    Her alan tip denetimine tabidir. (örnek: str, int, bool)
    """

    # model_config → Pydantic'in çalışma şeklini ayarlıyoruz
    model_config = SettingsConfigDict(
        env_file=".env",  # .env dosyasından değişkenleri oku
        env_file_encoding="utf-8",  # Türkçe karakter desteği
        extra="ignore",  # Bilinmeyen değişkenleri yok say
    )

    # Uygulama genel ayarları
    app_name: str = "learnpyapp"  # Uygulama adı
    app_env: str = "dev"  # Ortam (dev | prod)
    log_level: str = "INFO"  # Log seviyesi


# 🌍 Global ayar nesnesi oluştur
settings = Settings()
