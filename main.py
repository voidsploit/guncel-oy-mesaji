import requests
import json
from datetime import datetime
import time
def virgul_ekle(sayi):
    sayi = str(sayi)
    n = len(sayi)
    virgullu_sayi = ""
    
    for i in range(n):
        virgullu_sayi += sayi[i]
        if (n - i - 1) % 3 == 0 and i != n - 1:
            virgullu_sayi += "."
    
    return virgullu_sayi
webhook_url = 'WEBHOOK-LINKI'
headers = {
    'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
    'Accept': 'application/json',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://www.indyturk.com',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.indyturk.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close'
}
def mesajgonder():
    response = requests.get('https://scdn.ankahaber.net/secimsonuc/site/web/cb-overview.json?v=1684096909599', headers=headers)
    data = response.json()

    toplam_sandik = data['ToplamSandik']
    toplam_secmen = data['ToplamSecmen']
    acilan_sandik_secmen_sayisi = data['AcilanSandikSecmenSayisi']
    sonuclar = data['Sonuclar']

    embed = {
        'title': 'Oy Sonuçları',
        'color': 0x00ff00,  # Embed rengini belirleyebilirsiniz
        'fields': []
    }

    for sonuc in sonuclar:
        kod = sonuc['Kod']
        adi = sonuc['Adi']
        kisaltma = sonuc['Kisaltma']
        oy_orani = sonuc['OyOrani']
        oy_adedi = virgul_ekle(sonuc['OyAdedi'])
        if kod == 41: 
            recep = sonuc['OyAdedi']
            field = {
                'name': f':bulb:{adi}:bulb:',
                'value': f'Kısaltma: {kisaltma}\nOy Oranı: %{oy_orani}\nOy Adedi: {oy_adedi}',
                'inline': False
            }
        elif kod == 43: 
            kk = sonuc['OyAdedi']
            field = {
                'name': f':flag_tr: {adi} :flag_tr:',
                'value': f'Kısaltma: {kisaltma}\nOy Oranı: %{oy_orani}\nOy Adedi: {oy_adedi}',
                'inline': False
            } 
        else:
            field = {
                'name': f':clown: {adi} :clown:',
                'value': f'Kısaltma: {kisaltma}\nOy Oranı: %{oy_orani}\nOy Adedi: {oy_adedi}',
                'inline': False
            } 
        embed['fields'].append(field)

    embed['fields'].append({
        'name': 'Toplam Sandık',
        'value': str(virgul_ekle(toplam_sandik)),
        'inline': True
    })

    embed['fields'].append({
        'name': 'Toplam Seçmen',
        'value': str(virgul_ekle(toplam_secmen)),
        'inline': True
    })

    embed['fields'].append({
        'name': 'Açılan Sandık Seçmen Sayısı',
        'value': str(virgul_ekle(acilan_sandik_secmen_sayisi)),
        'inline': True
    })

    if recep > kk:
        fark = recep - kk
        embed['fields'].append({
            'name': 'rte ve kk Arasındaki Oy Farkı(kk>rte)',
            'value': str(virgul_ekle(fark)),
            'inline': True
        })
    else:
        fark = kk - recep
        embed['fields'].append({
            'name': 'rte ve kk Arasındaki Oy Farkı(rte>kk)',
            'value': str(virgul_ekle(fark)),
            'inline': True
        })

    # Tarih ve saat bilgisini almak
    tarih_ve_saat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    embed['fields'].append({
        'name': 'Tarih ve Saat',
        'value': tarih_ve_saat,
        'inline': True
    })

    embed['fields'].append({
        'name': 'Bu mesaj 30 saniye sonra tekrar gonderilecektir',
        'value': '',
        'inline': True
    })

    payload = {
        'embeds': [embed]
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 204:
        print('Sonuçlar başarıyla gönderildi.')
    else:
        print('Sonuçları gönderirken bir hata oluştu.')

while True:
    mesajgonder()
    time.sleep(30)