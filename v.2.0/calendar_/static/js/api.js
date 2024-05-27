function API()
{

    this.getListSpecialist = function(successHandler, failHandler)//successHandler, failHandler - эти переменные содержат ссылки на функции
    //successHandler - выводит данные если их удалось получиить, failHandler - выводит ошибку если их не удалось получить
    {
        let response = fetch("/specialist/");//отправка гет запроса на сервер по пути /specialist/ (смотри код в питоне, файл urls.py в папке appointment)
        response.then(r => this.processResponse(r, successHandler, failHandler));
        //смысл строки - дождаться данных от сервера и запустить код в функции processResponse (смотри ниже)
        // then - дождаться завершения предыдущего действия и начать следущее
        //r => this.processResponse - вызываем функцию processResponse
    }

    this.getCalendarSpecialist = function(specialist_id, online, successHandler, failHandler)
    {
        let today = formatDate(new Date());//получаем текущую дату
        let dayAfterThreeMonth = formatDate(new Date(new Date().setDate(new Date().getDate() + 90)));//текущая дата + 90 дней (срок действия открытого таймслота)
        // new Date().getDate() - получение текущей даты с компа по настройкам браузера, new Date().setDate - выставить текущую дату
        let body = {"begin": today, "end": dayAfterThreeMonth, "specialist_id": specialist_id, "online": online};
        //создаем обьект по правилам синтаксиса джава скрипта
        let bodyJSON = JSON.stringify(body);// созданный обьект на 19ой строке преобразуем в JSON формат
        let response = fetch('/get_freedate_list/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: bodyJSON
        });
        response.then(r => this.processResponse(r, successHandler, failHandler));
    }

    this.processResponse = function(response, successHandler, failHandler)// response - ответ сервера, который был получен на предыдущем шаге    
    // дальше функция проверяет ответ сервера на корректность
    {
        if(!response.ok){
            // если сервер не вернул ответ 200 (то есть вернул неуспех), то вызываем failHandler передавая туда код статуса
            failHandler(response.status);
        }
        else{
            response.json().then(successHandler);//берем тело обьекта, преобразуем в джаваскрипт обьект и передаем внутрь successHandler
        }
    }

    this.getTimeSlotBySpecialistIdAndDate = function(specialist_id, date, online, successHandler, failHandler)
    {
        let body = {"specialist_id": specialist_id, "date": date, "online": online};
        let bodyJSON = JSON.stringify(body);
        let response = fetch('/get_time_slot/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: bodyJSON
        });
        response.then(r => this.processResponse(r, successHandler, failHandler));
    }

    this.validatePhone = function(phone, successHandler, failHandler)
    {
        let body = {"phone": phone};
        let bodyJSON = JSON.stringify(body);
        let response = fetch('/validation_phone_number/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: bodyJSON
        });
        response.then(r => this.processResponse(r, successHandler, failHandler));
    }

    this.apointmentSignUp = function(data, successHandler, failHandler)
    {
        let bodyJSON = JSON.stringify(data);
        let response = fetch('/appointment/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: bodyJSON
        });
        response.then(r => this.processResponse(r, successHandler, failHandler));
    }
}
