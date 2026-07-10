# Yemek Tarifi Platformu (Flask)

Flask ile geliştirilmiş, kullanıcıların yemek tarifi paylaşabildiği, birbirleriyle gerçek zamanlı sohbet edebildiği tam kapsamlı bir web uygulaması.

## Özellikler

- **Kullanıcı Yönetimi:** Kayıt olma, giriş yapma ve OAuth ile üçüncü parti hesaplarla oturum açma
- **Gerçek Zamanlı Sohbet:** WebSocket tabanlı canlı mesajlaşma sistemi
- **Tarif Yönetimi:** Yemek tarifi ekleme, silme ve listeleme
- **Etkileşim:** Tariflere yorum yapma
- **Profil Yönetimi:** Kullanıcı profili üzerinde tam CRUD (oluşturma, okuma, güncelleme, silme) işlemleri

## Kullanılan Teknolojiler

- **Backend:** Python, Flask
- **Gerçek Zamanlı İletişim:** WebSocket
- **Kimlik Doğrulama:** OAuth

## Kurulum

```bash
git clone https://github.com/GuvenEminSamil/python_project.git
cd python_project
pip install -r requirements.txt
python app.py
```

## Not

Bu proje, aynı işlevselliğin Spring Boot ile geliştirilmiş bir versiyonuyla birlikte, farklı teknoloji yığınlarında aynı problemi çözme pratiği amacıyla hazırlanmıştır.
