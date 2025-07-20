# MCP Banking Backend - FastAPI & AI Integration

🏦 **Kapsamlı fintech backend sistemi** - FastAPI, SQLite veritabanı, JWT kimlik doğrulama, HTTP-only çerezler, sahte banka entegrasyonu ve **Model Context Protocol (MCP)** ile AI agent entegrasyonu içeren güvenli bankacılık operasyonları platformu.

## 🏗️ Sistem Mimarisi

```text
React Frontend → FastAPI Backend → MCP AI Agents → External Bank API
       ↓              ↓                ↓              ↓
   Web Client    Auth + DB        AI Analysis    Portfolio Data
```

### 📋 Bileşenler
- **🎨 Frontend**: React uygulaması (localhost:3000) - Kullanıcı arayüzü
- **🚀 Backend**: FastAPI sunucusu (localhost:8000) - Ana API ve veritabanı
- **🤖 MCP Server**: Node.js AI agent sunucusu (localhost:8001) - Finansal AI analizi
- **🏦 Dummy Bank**: Mock banking API (localhost:3000) - Portfolio verileri
- **🧠 AI Agents**: LLM destekli finansal danışmanlık ve analiz

## ✨ Özellikler

### 🔐 **Güvenlik ve Kimlik Doğrulama**
- **Çifte Kimlik Doğrulama**: JWT token + HTTP-only çerezler
- **Güvenli Oturum Yönetimi**: Cookie-based authentication web tarayıcıları için
- **Kullanıcı Yetkilendirmesi**: Korumalı endpoint'ler ve sahiplik doğrulaması
- **Şifre Hashleme**: bcrypt ile güvenli şifre saklama

### 💾 **Veritabanı ve Veri Yönetimi**
- **SQLite Veritabanı**: Kullanıcı hesapları, işlemler ve bankacılık verileri
- **SQLAlchemy ORM**: Type-safe veritabanı işlemleri
- **CustomerOID Senkronizasyonu**: Harici banka sistemleri ile otomatik bağlantı
- **Gerçek Zamanlı Veriler**: Canlı hesap bakiyeleri ve işlem takibi

### 🏦 **Bankacılık İşlemleri**
- **Hesap Yönetimi**: Çoklu hesap desteği, bakiye takibi
- **Para Transferleri**: Hesaplar arası güvenli transfer işlemleri
- **İşlem Geçmişi**: Detaylı işlem kayıtları ve filtreleme
- **Portfolio Entegrasyonu**: Harici banka API'si ile tam entegrasyon

### 🤖 **AI-Powered Finansal Analiz**
- **Portfolio Analizi**: Yatırım portföyü değerlendirmesi ve önerileri
- **Risk Analizi**: Volatilite hesaplama ve risk değerlendirmesi
- **Piyasa Analizi**: Gerçek zamanlı piyasa verileri ile analiz
- **Akıllı Sohbet**: Doğal dil ile finansal danışmanlık

### 🔗 **Entegrasyonlar**
- **MCP Protocol**: AI agent sistemi ile seamless entegrasyon
- **Finnhub API**: Gerçek zamanlı borsa verileri
- **LangChain + Ollama**: Yerel AI model desteği
- **CORS Desteği**: Frontend-backend güvenli iletişimi

## 🚀 Hızlı Başlangıç

### ⚙️ Gereksinimler

**Sistem Gereksinimleri:**
- Python 3.8+
- Node.js 18+ (MCP Server için)
- SQLite3
- Git

**Harici Servisler:**
- Ollama (AI modeli için) - `ollama pull gemma3:4b`
- Finnhub API Key (piyasa verileri için)

### 📦 Kurulum

#### 1. **Proje Kurulumu**
```bash
# Repository'yi klonlayın
git clone <repo-url>
cd mcpOpenbankingBackend

# Python sanal ortamı oluşturun
python -m venv venv

# Sanal ortamı aktifleştirin
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

#### 2. **Ortam Yapılandırması**
`.env` dosyası oluşturun:
```env
# Database
DATABASE_URL=sqlite:///./banking.db

# JWT Security
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
DUMMY_BANK_URL=http://localhost:3000
MCP_SERVER_URL=http://localhost:8001

# Optional: Finnhub API for market data
FINNHUB_API_KEY=your_finnhub_api_key
```

#### 3. **Sunucu Başlatma**

**Otomatik (Önerilen):**
```bash
# Windows
start_server.bat

# PowerShell
.\start_server.ps1
```

**Manuel:**
```bash
# FastAPI sunucusunu başlatın
python main.py

# Alternatif:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. **API Erişimi**
- 🌐 **API Server**: http://localhost:8000
- 📚 **API Dokümantasyonu**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/health
- 🗄️ **Veritabanı**: Otomatik oluşturulur ve örnek verilerle doldurulur

### 🔑 Test Kullanıcıları

Sistem otomatik olarak test kullanıcıları oluşturur:

| Kullanıcı Adı | Şifre | Rol |
|---------------|-------|-----|
| `john_doe` | `password123` | Standart Kullanıcı |
| `jane_smith` | `password123` | Standart Kullanıcı |

## 📡 API Endpoints

### 🔐 **Kimlik Doğrulama**

#### Kullanıcı Kaydı
```http
POST /register
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com", 
  "password": "securepassword",
  "full_name": "New User"
}
```

#### Giriş (JWT Token)
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=password123
```

#### Giriş (HTTP-Only Cookie)
```http
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}
```

#### Çıkış
```http
POST /logout
```

### 🏦 **Bankacılık İşlemleri**

#### Hesap Listesi
```http
GET /accounts
Authorization: Bearer <token>
```

#### Yeni Hesap Oluştur
```http
POST /accounts
Authorization: Bearer <token>
Content-Type: application/json

{
  "account_name": "Savings Account",
  "account_type": "savings",
  "currency": "USD"
}
```

#### Para Transferi
```http
POST /transfer
Authorization: Bearer <token>
Content-Type: application/json

{
  "from_account_id": "ACC001001",
  "to_account_id": "ACC001002", 
  "amount": 1000.00,
  "description": "Monthly savings"
}
```

#### İşlem Geçmişi
```http
GET /transactions/{account_id}?limit=10
Authorization: Bearer <token>
```

### 🤖 **AI & MCP Entegrasyonu**

#### MCP Agent Sorgusu
```http
POST /mcp/query
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "Portföyümü analiz edebilir misin?"
}
```

**Örnek AI Sorguları:**
- `"Yatırım portföyümü değerlendir"`
- `"Risk seviyemi analiz et"`
- `"Hangi hisse senetlerini almalıyım?"`
- `"Piyasa durumu nasıl?"`

#### Portfolio Özeti
```http
GET /portfolio-summary
Authorization: Bearer <token>
```

#### Kullanıcı Bilgileri
```http
GET /me
Authorization: Bearer <token>
```

### 🏥 **Sistem Endpoints**

#### Health Check
```http
GET /health
```

#### API Bilgileri
```http
GET /
```

## 🤖 AI Agent Sistemi

### **Master Agent Router**
Gelen sorguları analiz ederek uygun uzman ajana yönlendirir:

```python
# Sorgu türlerine göre yönlendirme
"portföy analizi" → Portfolio Analysis Agent
"risk değerlendirme" → Risk Analysis Agent  
"genel soru" → General Chatbot Agent
```

### **Uzman Ajanlar**

#### 📊 **Portfolio Analysis Agent**
- Yatırım portföyü analizi
- Diversifikasyon önerileri
- Performance değerlendirmesi
- Rebalancing stratejileri

#### ⚠️ **Risk Analysis Agent**
- Volatilite hesaplama
- Value at Risk (VaR) analizi
- Sektör konsantrasyon riski
- Stress test senaryoları

#### 💬 **General Chatbot Agent**
- Genel finansal sorular
- Piyasa bilgilendirmesi
- Eğitim içerikleri
- Kullanıcı desteği

### **Piyasa Verisi Entegrasyonu**
```javascript
// Finnhub API ile gerçek zamanlı veriler
- Hisse senedi fiyatları
- Değişim oranları (%change)
- İşlem hacmi
- Piyasa kapitalizasyonu
```

## 🧪 Test Etme

### **Otomatik Test Suite**
```bash
# Tüm testleri çalıştır
python -m pytest

# Specific test dosyaları
python test_main.py              # Ana API testleri
python test_mcp_integration.py   # MCP entegrasyon testleri
python test_cookie_auth.py       # Cookie authentication testleri
python test_bank_integration.py  # Banka entegrasyon testleri
```

### **Manuel API Testleri**

#### **Postman Collection Örneği**
```bash
# 1. Kullanıcı kaydı
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "test123", "full_name": "Test User"}'

# 2. Giriş yapma
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "test123"}' \
  -c cookies.txt

# 3. AI sorgusu (cookie ile)
curl -X POST "http://localhost:8000/mcp/query" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"query": "Portföyümü analiz et"}'
```

### **Frontend Entegrasyon Testi**
```javascript
// React frontend'den API çağrısı
const response = await fetch('http://localhost:8000/mcp/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include', // Cookie authentication
  body: JSON.stringify({ query: "Risk analizi yap" })
});

const result = await response.json();
console.log(result.response); // AI agent yanıtı
```

## 🗄️ Veritabanı Şeması

### **User Tablosu**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    customer_oid VARCHAR UNIQUE,  -- Dummy Bank CustomerOID
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Account Tablosu**
```sql
CREATE TABLE accounts (
    id VARCHAR PRIMARY KEY,        -- ACC001001 format
    account_name VARCHAR NOT NULL,
    account_type VARCHAR NOT NULL, -- checking, savings, credit
    balance FLOAT DEFAULT 0.0,
    currency VARCHAR DEFAULT 'USD',
    is_active BOOLEAN DEFAULT TRUE,
    user_id INTEGER REFERENCES users(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Transaction Tablosu**
```sql
CREATE TABLE transactions (
    id VARCHAR PRIMARY KEY,             -- TXN001001 format
    from_account_id VARCHAR REFERENCES accounts(id),
    to_account_id VARCHAR REFERENCES accounts(id),
    amount FLOAT NOT NULL,
    currency VARCHAR DEFAULT 'USD',
    description VARCHAR,
    transaction_type VARCHAR NOT NULL,  -- transfer, deposit, withdrawal
    status VARCHAR DEFAULT 'pending',   -- pending, completed, failed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🏗️ Proje Yapısı

```
mcpOpenbankingBackend/
├── main.py                 # 🚀 Ana FastAPI uygulaması
├── auth.py                 # 🔐 Kimlik doğrulama utilities
├── database.py             # 🗄️ SQLAlchemy modelleri ve DB config
├── schemas.py              # 📋 Pydantic request/response modelleri
├── bank_client.py          # 🏦 Harici banka API entegrasyonu
├── config.py               # ⚙️ Uygulama konfigürasyonu
├── requirements.txt        # 📦 Python bağımlılıkları
├── start_server.bat        # 🚀 Windows başlatma scripti
├── start_server.ps1        # 🚀 PowerShell başlatma scripti
├── reset_database.py       # 🔄 Veritabanı reset utility
├── test_*.py              # 🧪 Test dosyaları
├── banking.db             # 📄 SQLite veritabanı (otomatik oluşur)
├── API_REFERENCE.md       # 📚 Detaylı API dokümantasyonu
├── QUICKSTART.md          # ⚡ Hızlı başlangıç rehberi
├── CHANGELOG.md           # 📝 Versiyon geçmişi
└── __pycache__/           # 🐍 Python cache dosyaları
```

### **Dosya Açıklamaları**

**`main.py`** - Ana uygulama dosyası
- FastAPI app konfigürasyonu
- CORS middleware
- Tüm API endpoint'leri
- MCP agent entegrasyonu

**`auth.py`** - Kimlik doğrulama sistemi
- JWT token yönetimi
- Password hashing (bcrypt)
- User authentication utilities
- Cookie-based auth desteği

**`database.py`** - Veritabanı yönetimi
- SQLAlchemy model tanımları
- Database session yönetimi
- Tablo oluşturma ve initialization
- Sample data seeding

**`schemas.py`** - Pydantic modelleri
- Request/response type definitions
- Data validation schemas
- API contract definitions

**`bank_client.py`** - Harici banka entegrasyonu
- Dummy bank API client
- CustomerOID management
- Portfolio data fetching
- Error handling ve fallbacks

## 🚨 Sorun Giderme

### **Yaygın Sorunlar ve Çözümleri**

#### 🐛 **Database Locked Hatası**
```bash
# Veritabanını resetleyin
python reset_database.py

# Veya manuel olarak silin
rm banking.db
python main.py  # Yeniden oluşturur
```

#### 🔌 **MCP Server Bağlantı Hatası**
```bash
# MCP Node.js sunucusunun çalıştığını kontrol edin
curl http://localhost:8001/health

# Node.js serverini başlatın
cd ../mcpServerNode
npm start
```

#### 🚪 **Port Çakışması**
```bash
# Portu kontrol edin
netstat -an | findstr :8000

# Farklı port kullanın
uvicorn main:app --host 0.0.0.0 --port 8080
```

#### 🍪 **Cookie Authentication Sorunu**
```bash
# Tarayıcı geliştirici araçlarında cookies kontrolü
# Application > Cookies > localhost:8000
# access_token cookie'sinin var olduğunu kontrol edin

# Veya manual cookie test
curl -c cookies.txt -b cookies.txt http://localhost:8000/me
```

#### 🔐 **JWT Token Süresi Dolması**
```python
# auth.py dosyasında token süresini artırın
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 saat
```

### **Log ve Debug**

#### **Uygulama Logları**
```python
# main.py dosyasında log seviyesini artırın
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### **Database Query Logları**
```python
# database.py dosyasında SQL query loglarını aktifleştirin
engine = create_engine(DATABASE_URL, echo=True)  # echo=True ekleyin
```

## 🔒 Güvenlik Önerileri

### **Production Hazırlığı**

#### **Environment Variables**
```env
# Production değerleri
SECRET_KEY=super-secure-random-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=15
HTTPS_ONLY=true
SECURE_COOKIES=true
```

#### **Database Güvenliği**
```python
# PostgreSQL kullanın (SQLite yerine)
DATABASE_URL=postgresql://user:password@localhost/banking_db

# Connection pooling ekleyin
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
```

#### **HTTPS ve SSL**
```python
# SSL termination ile
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

#### **Rate Limiting**
```python
# slowapi ile rate limiting ekleyin
from slowapi import Limiter, _rate_limit_exceeded_handler

limiter = Limiter(key_func=get_remote_address)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/login")
@limiter.limit("5/minute")  # Dakikada 5 login denemesi
async def login(...):
    pass
```

## 📈 Performance Optimizasyonu

### **Database Optimizasyonu**
```python
# Index'ler ekleyin
class User(Base):
    username = Column(String, unique=True, index=True)  # Index eklendi
    customer_oid = Column(String, unique=True, index=True)

# Query optimizasyonu
@app.get("/accounts")
async def get_accounts(db: Session = Depends(get_db)):
    # Eager loading ile N+1 problem çözümü
    return db.query(Account).options(joinedload(Account.owner)).all()
```

### **Caching**
```python
# Redis cache ekleme
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expire_time=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            redis_client.setex(cache_key, expire_time, json.dumps(result))
            return result
        return wrapper
    return decorator

@app.get("/portfolio-summary")
@cache_result(expire_time=60)  # 1 dakika cache
async def get_portfolio_summary(...):
    pass
```

### **Async Optimizasyonu**
```python
# Database connection pooling
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(
    "sqlite+aiosqlite:///./banking.db",
    pool_size=20,
    max_overflow=0
)

# Bulk operations
@app.post("/bulk-transfer")
async def bulk_transfer(transfers: List[TransferRequest]):
    async with async_engine.begin() as conn:
        for transfer in transfers:
            await conn.execute(insert(Transaction).values(**transfer.dict()))
```

## 🔮 Gelecek Geliştirmeler

### **Kısa Vadeli (1-2 Ay)**
- [ ] **Real-time WebSocket** desteği (canlı bildirimler)
- [ ] **Redis Cache** entegrasyonu (performance artışı)
- [ ] **Email Notifications** (işlem bildirimleri)
- [ ] **2FA Authentication** (iki faktörlü kimlik doğrulama)
- [ ] **API Rate Limiting** (güvenlik artışı)

### **Orta Vadeli (3-6 Ay)**
- [ ] **PostgreSQL Migration** (production-ready database)
- [ ] **Docker Containerization** (deployment kolaylığı)
- [ ] **Kubernetes Support** (scalability)
- [ ] **Advanced Analytics** (machine learning entegrasyonu)
- [ ] **Mobile API Support** (React Native için optimize edilmiş)

### **Uzun Vadeli (6+ Ay)**
- [ ] **Microservices Architecture** (modüler sistem)
- [ ] **Event Sourcing** (audit trail ve rollback)
- [ ] **CQRS Pattern** (command-query separation)
- [ ] **GraphQL API** (flexible data fetching)
- [ ] **Blockchain Integration** (decentralized features)

### **AI & ML Geliştirmeleri**
- [ ] **Fraud Detection** (yapay zeka tabanlı dolandırıcılık tespiti)
- [ ] **Personalized Recommendations** (kişiselleştirilmiş yatırım önerileri)
- [ ] **Predictive Analytics** (gelecek trend tahminleri)
- [ ] **Natural Language Processing** (gelişmiş sohbet botu)
- [ ] **Automated Portfolio Rebalancing** (otomatik portföy yeniden dengeleme)

## 🤝 Katkıda Bulunma

### **Geliştirme Süreci**
1. **Fork** edin repository'yi
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** yapın değişikliklerinizi (`git commit -m 'Add amazing feature'`)
4. **Push** edin branch'e (`git push origin feature/amazing-feature`)
5. **Pull Request** açın

### **Code Standards**
```python
# Type hints kullanın
async def get_user(user_id: int, db: Session) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

# Docstring ekleyin
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate user with username and password.
    
    Args:
        db: Database session
        username: User's username
        password: Plain text password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    pass

# Error handling
try:
    result = await some_operation()
except SpecificException as e:
    logger.error(f"Specific operation failed: {e}")
    raise HTTPException(status_code=400, detail="Operation failed")
```

### **Test Coverage**
```bash
# Test coverage raporu
pip install pytest-cov
pytest --cov=. --cov-report=html

# Test yazma örneği
def test_create_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com", 
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
```

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## 🆘 Destek ve İletişim

### **Sorun Bildirimi**
- 🐛 **Bug Reports**: GitHub Issues kullanın
- 💡 **Feature Requests**: GitHub Discussions
- 📚 **Dokümantasyon**: Wiki sayfalarını kontrol edin

### **Geliştirici Desteği**
- 📧 **Email**: developer@mcpbanking.com
- 💬 **Discord**: MCP Banking Community
- 🐦 **Twitter**: @MCPBanking

### **Topluluk**
- 🌟 **GitHub Stars**: Projeyi beğendiyseniz star verin
- 🍴 **Forks**: Kendi versiyonunuzu oluşturun
- 📢 **Share**: Arkadaşlarınızla paylaşın

---

**⚠️ Not**: Bu proje eğitim ve demonstrasyon amaçlıdır. Production ortamında kullanmadan önce güvenlik review yapın ve production-ready konfigürasyonları uygulayın.

**🚀 Happy Coding!** - MCP Banking Team

- `POST /register` - Register new user (with dummy bank sync)
- `POST /token` - Login with form data (sets HTTP-only cookie)
- `POST /login` - Login with JSON (sets HTTP-only cookie)
- `POST /logout` - Logout (clears HTTP-only cookie)

### User & Account Management

- `GET /me` - Get current user info
- `GET /accounts` - Get user's accounts
- `GET /accounts/{account_id}` - Get account details
- `GET /accounts/{account_id}/balance` - Get account balance
- `GET /accounts/{account_id}/transactions` - Get transaction history

### Banking Operations

- `POST /transfer?from_account_id={id}` - Transfer money between accounts

### Dummy Bank Integration

- `GET /bank/portfolio` - Get user's portfolio from dummy bank
- `GET /bank/status` - Check dummy bank connection status
- `GET /bank/customers` - Get all customers from dummy bank (admin)
- `POST /bank/sync` - Sync current user with dummy bank

### MCP Integration

- `GET /mcp/status` - Get MCP server status
- `POST /mcp/query` - Query MCP agent with natural language

### Admin & Health

- `GET /health` - System health check (includes all service statuses)
- `GET /admin/users` - Get all users
- `POST /config` - Update MCP server configuration

## 🧪 Usage Examples

### Register New User

```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "newuser",
       "email": "user@example.com", 
       "password": "securepass123",
       "full_name": "New User"
     }'
```

### Get Account Balance (with authentication)

```bash
# First get token
TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=password123" | jq -r .access_token)

# Then get balance
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/accounts/ACC001/balance"
```

### Transfer Money

```bash
curl -X POST "http://localhost:8000/transfer?from_account_id=ACC001" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "to_account_id": "ACC002",
       "amount": 100.00,
       "currency": "USD",
       "description": "Transfer to savings"
     }'
```

### Cookie Authentication (Web Browsers)

```bash
# Login with JSON and receive HTTP-only cookie
curl -c cookies.txt -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "password123"
     }'

# Use cookie for subsequent requests
curl -b cookies.txt "http://localhost:8000/me"

# Logout (clears cookie)
curl -b cookies.txt -c cookies.txt -X POST "http://localhost:8000/logout"
```

### Bank Integration Examples

```bash
# Get user's portfolio from dummy bank
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/bank/portfolio"

# Sync current user with dummy bank
curl -X POST "http://localhost:8000/bank/sync" \
     -H "Authorization: Bearer $TOKEN"

# Check dummy bank connection
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/bank/status"
```

## 🗄️ Database Schema

### Users Table

- `id`, `username`, `email`, `hashed_password`, `full_name`, `customer_oid`, `is_active`, `created_at`

### Accounts Table

- `id`, `account_name`, `account_type`, `balance`, `currency`, `user_id`, `is_active`, `created_at`

### Transactions Table

- `id`, `from_account_id`, `to_account_id`, `amount`, `currency`, `description`, `transaction_type`, `status`, `created_at`

**Note**: The `customer_oid` field links local users to external dummy bank customers for portfolio synchronization.

## 🤖 MCP Integration

The backend automatically notifies MCP agents about:

- Account access and balance checks
- Transaction history requests
- Money transfers and fraud detection
- User authentication events

MCP agents can provide:

- Real-time fraud detection
- Transaction categorization
- Spending analysis
- Account recommendations

## 📁 Project Structure

```text
mcpOpenbankingBackend/
├── main.py              # Main FastAPI application with dual authentication
├── database.py          # SQLAlchemy models and database setup with CustomerOID
├── auth.py              # JWT + Cookie authentication utilities
├── schemas.py           # Pydantic request/response models
├── bank_client.py       # Dummy bank API integration client
├── test_server.py       # Comprehensive test suite
├── test_cookie_auth.py  # Cookie authentication testing
├── reset_database.py    # Database reset with dummy bank sync
├── requirements.txt     # Python dependencies
├── environment.yaml     # Conda environment specification
├── start_server.bat     # Easy startup script
├── .gitignore          # Git ignore rules
└── banking.db          # SQLite database (auto-created)
```

## 🔧 Configuration

- **JWT Secret**: Change `SECRET_KEY` in `auth.py` for production
- **Database**: SQLite file `banking.db` (automatically created)
- **MCP Server**: Configured for port 8001 (update via `/config` endpoint)
- **Dummy Bank**: External API on port 3000 for portfolio data
- **Cookies**: HTTP-only, SameSite=lax (set secure=True for HTTPS in production)

## 🛡️ Security Features

- **Dual Authentication**: JWT Bearer tokens + HTTP-only cookies
- **Password Security**: bcrypt hashing with salt
- **Session Management**: Secure cookie configuration with proper flags
- **Authorization**: User ownership validation for all operations
- **Protected Endpoints**: Dependency injection for authentication
- **CORS**: Configurable for production environments
- **Database Security**: Automatic relationship enforcement and input validation
- **External API**: Secure integration with dummy bank using CustomerOID linking

## 🧪 Testing & Development

### Cookie Authentication Testing

```bash
# Run cookie authentication tests
python test_cookie_auth.py
```

### Postman Testing

The API supports both authentication methods:

- **Bearer Token**: Add `Authorization: Bearer <token>` header
- **Cookies**: Postman automatically handles cookies after login

### Database Reset

```bash
# Reset database with dummy bank integration
python reset_database.py
```

### Run Comprehensive Tests

```bash
# Run all tests
python test_server.py
```

This will test:

- Authentication flow
- Account operations
- Money transfers
- User registration
- Cookie authentication
- Bank integration

## 🚀 External Integrations

### MCP Server (Port 8001)

- Banking agent operations
- Fraud detection
- Transaction analysis
- Natural language queries

### Dummy Bank API (Port 3000)

- Customer registration with CustomerOID
- Portfolio data retrieval
- Account synchronization
- Connection health monitoring

## 📊 Health Monitoring

Access the health endpoint to check all service statuses:

```bash
curl http://localhost:8000/health
```

Returns status for:

- FastAPI backend
- SQLite database
- MCP server connection
- Dummy bank API connection

## 🔄 Development Workflow

1. **Start External Services** (optional):
   - MCP Server on port 8001
   - Dummy Bank API on port 3000

2. **Initialize Backend**:

   ```bash
   python main.py
   ```

3. **Test Authentication**:

   ```bash
   python test_cookie_auth.py
   ```

4. **Reset Database** (if needed):

   ```bash
   python reset_database.py
   ```

5. **Access API Documentation**: <http://localhost:8000/docs>

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests to ensure functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
