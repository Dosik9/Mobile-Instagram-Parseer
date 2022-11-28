<h1 align="center">Hi there, I'm <a href="https://daniilshat.ru/" target="_blank">Dosbol</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

# Mobile-Instagram-Parseer
This software can parsing followers and followings from instagram 

Перед тем как запустить этот код, вам нужно:
  1.	Установить JDK 
  a.	(лучше старую версию, а то будут проблемы с Android Studio)
  2.	Работа с средами переменных ![image](https://user-images.githubusercontent.com/57053315/204222288-2b89b46a-08cc-4953-ad44-cd72e2b32784.png), установить Path правильно (https://www.youtube.com/watch?v=V44V-HPqmaM хороший туториал вроде)  
  3.	Установка Android Studio
  4.	Еще раз работа с 2 пунктом
  5.	Установка Appium
  6.	Appium Inspector (можно и установить десктопную версию (https://github.com/appium/appium-desktop ) или работать онлайн (https://inspector.appiumpro.com/ ))
  7.	Через Android Studio создать/открыть необходимый девайс ![image](https://user-images.githubusercontent.com/57053315/204222395-d8231a79-94c2-44d6-bc4c-bb8c6182cccd.png)
  8.	Основная работа на Python, откроем редактор кода 
  9.	Import Packages ![image](https://user-images.githubusercontent.com/57053315/204222461-8202448a-2e58-46a1-998a-920d1aa7263c.png)  
  10.	Appium start server
  11.	Связка с девайсом, которую мы создали на Android Studio. Чтот показано со стрелками это и есть связка. Прростая линия - это связка с Appium. (http://127....... /../.. стандарт)![image](https://user-images.githubusercontent.com/57053315/204222530-df7d6ee2-1371-4901-9707-df131917a311.png)
  12.	Appium Inspector в действий. Это данные нашего девайса. ![image](https://user-images.githubusercontent.com/57053315/204223100-b14c11ad-ac2a-483f-9ab8-bea737c01960.png)

  13.	Start Session

Для полноценной работы у вас на девайсе должна быть установлено Instagram. Заходите в систему в ручную. Для парсинга аккаунта, аккаунт должен быть публичным. Вы также можете задать глубину парсинга, но по умолчанию оно парсить в 1 глубину


Немного по коду:
![image](https://user-images.githubusercontent.com/57053315/204223734-c82409d0-f824-4f60-b948-8b4157b226f1.png)
