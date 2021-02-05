# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 12:43:37 2021

Programa Tez dosyasını Word(docx) formatında vermelisiniz!
"""
import docx
from os import chdir
from snowballstemmer import TurkishStemmer
from nltk.tokenize import word_tokenize

# Os kütüphanesini kullanarak, dosyanın bulunduğu dizinin yoluna gidiyoruz.
chdir("C:/Users/Asus/Desktop/tokentry/")
class Token:
    
    """
    Sınıfın ismi Token. Konsolda çalıştırmak için Token'dan nesne türetilmesi gerekmekedir. (x = Token("TezDosyaAdı.docx"))
    Python'da __init__ yapıcı methoddur. Yapıcılar nesne türetilidiğinde otomatik olarak türetilecek değişkenleri veya işlemleri burada tanımlamaktayız.
    Sınıf türetilirken, dosyanın isminin yazılması 'path' değişkeninin yapıcı methoda parametre olarak verilmesinden kaynaklıdır.
    """
    def __init__(self,path):
        #Dosya Kanak Uzantısının yolu için kullanılır
        self.path = path
        #Boşluk Karakterleri - İndis numaraları düzenleme çin kullanılır
        self.sayac = 0
        #Tez dosyasını docx kütüphanesi ile kullanıma hazır hale getirtilir
        self.doc = docx.Document(path) 
        #Düzenleme işlemi olmadan tüm listeyi içerisinde barındırır
        self.allText = []
        #Pars işlemi uygulanan ayrıştırılmış listeyi barındırır
        self.parsText= []
        #Kaynakça yazılarını liste halinde barındırır
        self.KaynakcaText = []
        #Kaynakcanın başlangıç indisini tutar
        self.kaynak_indis = 0
        #KAynakçanın doğru yazılıp yazılmadığını liste halinde geri döndürür
        self.Kaynakca_Degerlist = []
        #Aranan Kelime olursa indis numaraını numara olarak geri dönderir 
        self.ArananKelimeList = []
        #önsöz başlangıç indisini saklar
        self.Onsoz =0
        #Ek bölümü varsa Ayırma işlemi için hafızada beklenir
        self.IndısEk = 0
        
        #İşlemlerin daha sağlıklı yapılabilmesi için. Gönderilen dosyayı program başlarken tanımlanan AllText listesinin içerisine aktarır
        for i in self.doc.paragraphs:
            self.allText.append(i.text)
    
    """Program hafızaya alındıktan sonra, .çalıştırılması gereken ilk parametredir. Bu parametre ile dosya içerisinde ayıklama ve 
    bilgilendirmeler yapılıp çıktı olarak kullanıcıya sunulur"""
    
    def DosyaDuzenle(self):
        #Kelimeleri eklerinden ayırıp köklerini ortaya çıkartır
        kelime = TurkishStemmer()
        #allText dosyası içerisinde dönmeye başlar. 
        for i in self.allText:
            #Boşluk karakterlerini araştırıyoruz
            if(i == "" or i == "\n"):
                pass
            #Boşluk karakteri olamadığı durumda düzenlenmiş dosyaya kelimeyi ekliyoruz 
            else:
                self.parsText.append(i)
        #Ayrılmış dosya içerisinde gezinmeye başlıyoruz. 
        for i in self.parsText:
            #Kelimelerin köklerini inceleyip ilgili kelimeyi bulduğu zaman değeri indis numarası olarak almakta. "Kaynakça" -> "kaynak"
            if (kelime.stemWord(i.lower()) == "kaynak"):
                self.kaynak_indis = self.sayac
            #Kelimelerin köklerini inceleyip ilgili kelimeyi bulduğu zaman değeri indis numarası olarak almakta. "Önsöz" -> "önsöz"
            if (kelime.stemWord(i.lower()) == "önsöz"):
                self.Onsoz = self.sayac
            #Kelimelerin köklerini inceleyip ilgili kelimeyi bulduğu zaman değeri indis numarası olarak almakta. "Ekler Bölümü" -> "ekler"    
            if (kelime.stemWord(i.lower()) == "ekler"):
                self.IndısEk = self.sayac
            else:
                self.sayac +=1 
        print("\t Toplam Boşluk Karakteri Sayısı: ",len(self.allText)-self.sayac)   
        print("\t Boşluk karakteri olmadan toplam satır sayısı: ",self.sayac)
        print("\t Kaynakca Başlangıç indisi: ",self.kaynak_indis)
        print("\t Onsoz Başlangıç indisi: ",self.Onsoz)
        print("\t Toplam Yapılan Atıf: ", (self.sayac - self.kaynak_indis))
    
    """DosyaDuzenle() Fonksiyonu çağırıldıktan sonra düzenlenmiş dosyayı çıktı olarak gösterir. 15.12.2020"""   
    def DosyaGoruntule(self):
        for i in range(len(self.parsText)):
            print(self.parsText[i])
        return len(self.parsText)
    
    """Fonksiyon bir değer yazılarak çağırılır. Parametre Düzenlenmiş listede ki satırı döndürür.23.12.2020"""
    def DosyaSatırOlarakGosterme(self,indis):     
        try:
            return self.parsText[indis]
        except TypeError:
            print( "Görüntülemek istediğiniz satırı giriniz!!")
        except:
            print("Bir şeyler Ters gidiyor")
            
    """Parçalanmamış Orjinal Dosyadan satır gösteriririz 23.12.2020"""
    def OrjinalDosyadanSatırGoster(self,indis):
        try:
            return self.allText[indis]
        except Exception:
            return "Giriş Hatası Yapıldı. Girişe dikka Edin!"
    
    """Fonksiyonun parametresine dosyanın satırının tamamı verildiğinde çıktı olarak indis numrasını döndürür"""
    def SatırİndisBul(self,kelime): 
        try:
            return(self.parsText.index(kelime))
        except ValueError:
            return "Kelime Bulunamadı!"
        
    """Fonksiyonun parametsine aranmak istenen kelime verilir. Çıktı olarak aranan kelime varsa satır numarasını döndürür."""    
    def KelimeArama(self,key):
       try:
        sayac = False
        for i in self.parsText:
            #Parçalanmış liste içerisinde döngüye gidiyoruz
            kelime = word_tokenize(str(i))
            #kelime değişkeni içerisinde döngüye giriyoruz.
            for j in kelime:
                #Eğer parametreye gönderilen değer kelime ile eşleşiyorsa sayac true dönerek  Aranankelime parametresine kelime 0 veya 1 kaydediyor. 
            
                if(j == key):
                  sayac = True
                  self.ArananKelimeList.append(self.parsText.index(i))           
                else:
                    pass 
        if(sayac == False):
            return"Aranılan Kelime Bulunamadı!"
        else:
            for i in set(self.ArananKelimeList):
                print("Satır Sırası: {}".format(i))
       except Exception:
           return "Giriş İçin Değer Verin!"
    
    #KelimeArama() fonksiyonu çalıştırılıp aranan kelimeler bir listeye atanır bu listeyi ArananKelimeSatır() fonksiyonu çağrılarak görüntülenebilir
    def ArananKelimeSatır(self):
        Keywords = set(self.ArananKelimeList)
        for i in Keywords:
            print(self.parsText[i],end = "\n \n")

    #Tez dosyası içerisinde ki "Kaynak" bölümünü arayıp kaynakça bölümünde sayfa belirtilmemişse hata satırlarını döndürür!
    def KaynakcaTarama(self):
        s=0
        for i in self.parsText[(self.kaynak_indis+1):]:
            words = word_tokenize(str(i))
            for j in words:
                if(j == "pp" or j == "ss" or j == "sayfa" or j == "page" or j == "syf"):
                    s+=1                
                else:
                    pass
            if(s>0):
                self.Kaynakca_Degerlist.append(1)
            else:
                self.Kaynakca_Degerlist.append(0)
            s=0
        g = len(self.Kaynakca_Degerlist)
        print(self.Kaynakca_Degerlist)
        return print("Kaynaklar/Kaynakca bölümünde toplam hata sayısı= ",g)
    #Fonksiyon tez dosyasının giriş Sayfasını kontrol eder.
    def GirisSayfası(self):
       try:
            dboll = False
            orjinal = ["T.C.","FIRAT ÜNİVERSİTESİ","FEN BİLİMLERİ ENSTİTÜSÜ"]
            for i in range(3):
                if(orjinal[i] == self.parsText[i]):
                    dboll = True
                else:
                    dboll = False
            if(dboll == False):
                return "Giriş Etikitetinde Uyumsuzluk Tespit Edildi!"
            print("Giriş İşlmeleri Doğru!")
       except Exception:
           pass
       finally:
           pass