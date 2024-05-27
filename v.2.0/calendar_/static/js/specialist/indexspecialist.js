
//сам бутстрап включается в хтмл файле
function SpecialistController(base_selector) {
    this.base_selector = base_selector;// this.base_selector - создали атрибут для дальнейшего использования, это поле которое будет хранить селектор и отдавать его тем функциям который им будет нужен, селектор - это последовательность символов позволяющая отличить один элемент от другого
    // this.api = new API();//создание обьекта по существующей функции в другом файле. Импорт происходит через хтмл файл. Смотри файл api.js
    this.specialistId = null;// обьявление переменной, this нужно для обозначентя области видимости этой переменной, она будет работать на уровне обьекта.
    this.token = null;// создали переменную для хранения токена специалиста. При отправке запроса мы должны передавать токен специалиста для его авторизации
    //почитать local storage js. https://learn.javascript.ru/localstorage
    this.start = function () {
        let token = localStorage.getItem(tokenKeyStorage);//получение токена из локалсторадж
        let usernameFirst = localStorage.getItem(userPsiUsername);//получение токена из локалсторадж

        if (token && usernameFirst) {
            document.body.innerHTML = "";
            loadSpecialist(token, usernameFirst, showSpecialist, null);
            return false; // нужно чтобы функция остановилась
        }
    }
    this.login = function () {

    }
    this.loadAuthData = function () {
        //let specialist_id = localStorage.getItem(specialistIdKeyStorage);//получение ай ди специалиста от сервера
        let token = localStorage.getItem(tokenKeyStorage);//получение токена из локалсторадж


        let username = document.getElementById('username');//получение введенного пользователем юзернейма
        let password = document.getElementById('auth_pass'); //получение введенного пользователем пароля



        if (!token && username && password) {

            username = username.value.trim();//trim - убрать пробелы в начале и конце строки
            password = password.value;

            if (username == "") {
                window.alert("вы не ввели имя пользователя");
                return false;// нужно чтобы функция остановилась
            }

            if (password == "") {
                window.alert("вы не ввели пароль");
                return false;// нужно чтобы функция остановилась
            }

            getToken(username, password, reloadPageAfterGetToken, showError);
        }

    }

}



function loadSpecialist(token, username, successFunc, failFunc) {
    const myHeaders = new Headers();//вынести в отдельную функцию которая принимает три параметра - токен, функция в слоучае успеха, функция в случае неудачи) 
    myHeaders.append('Content-Type', 'application/json');
    myHeaders.append('Authorization', 'Token ' + token);

    let body = { "e_mail": username };
    let bodyJSON = JSON.stringify(body);
    fetch('/specialistId/', {
        method: 'POST',
        headers: myHeaders,
        body: bodyJSON
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            //console.log(data);
            localStorage.setItem("specialist", JSON.stringify(data))
            successFunc(data);
            //вызываем переданную функцию успеха
        })
}

function reloadPageAfterGetToken(token, username) {
    localStorage.setItem(tokenKeyStorage, token);//здесь обрабатываем обьект и сохраняем все в localStorage
    localStorage.setItem(userPsiUsername, username);
    document.body.innerHTML = "";//если не добавить эту строку то на странице останется ненужная инфа
    loadSpecialist(token, username, showSpecialist, null);
}

function showError(error) {
    alert(error);
}

function getToken(username, password, successFunc, failFunc) {//successFunc, failFunc - это функции а не параметры
    //все что ниже вынести также в отдельную функцию с параметрами - юзернейм, пароль, функцию успеха, функцию неудачи
    var formData = new FormData();
    formData.append('username', username)
    formData.append('password', password)


    fetch('/api-token-auth/', {
        method: 'POST',
        body: formData
    })//на этом этапе происходит отправка запроса и получение ответа и предполагаем, что получем ответ в виде строки в формате json (для данного случая)
        .then(function (response) {
            return response.json();//здесь из ответа сервера в виде строки (см обьяснения выше) формируем js объект
        })
        .then(function (data) {
            if (!data.token) {
                //window.alert("вы ввели неверный логин или пароль");//вызвать функцию неудачи здесь
                failFunc("вы ввели неверный логин или пароль");
                return false;// нужно чтобы функция остановилась

            }

            //вызвать функцию успеха - функция сохраняет локал сторадж, очищает страницу и вызывает функцию №1

            successFunc(data.token, username);

        })
}


function logOut() {
    localStorage.removeItem(userPsiUsername);
    localStorage.removeItem(tokenKeyStorage);
    location.reload();


}

function getCalendarSpecialist(specialist_id, online, successHandler, failHandler) {
    let today = formatDate(new Date());//получаем текущую дату
    let dayAfterThreeMonth = formatDate(new Date(new Date().setDate(new Date().getDate() + 90)));//текущая дата + 90 дней (срок действия открытого таймслота)
    // new Date().getDate() - получение текущей даты с компа по настройкам браузера, new Date().setDate - выставить текущую дату
    let body = { "begin": today, "end": dayAfterThreeMonth, "specialist_id": specialist_id, "online": online };
    //создаем обьект по правилам синтаксиса джава скрипта
    let bodyJSON = JSON.stringify(body);// созданный обьект на 19ой строке преобразуем в JSON формат
    let response = fetch('/get_freedate_list/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: bodyJSON
    });
    //response.then(r => r.json()).then(r => console.log(r));
    response.then(r => r.json()).then(r => showCalendar(r));
}

function getTimeSlotBySpecialistIdAndDate(specialist_id, date, online, successHandler, failHandler) {
    let body = { "specialist_id": specialist_id, "date": date, "online": online };
    let bodyJSON = JSON.stringify(body);
    let response = fetch('/get_time_slot/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: bodyJSON
    });
    //response.then((r => r.json()).then(r => showTimeslot(r)));
    response.then(r => r.json()).then(r => successHandler(r));
}


function createTimeSlot(specialist_id, date, online, successHandler, failHandler){
    let requiredData = setDate(new Date());
    let requiredTime = setTime(new TimeRanges());
    let body = { "requiredData": requiredData, "requiredTime": requiredTime, "specialist_id": specialist_id, "online": online };
    let bodyJSON = JSON.stringify(body);
    let response = fetch('/   /', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: bodyJSON
    });
    response.then();


}


function showCalendar(listDate) {
    listDate = listDate.map(item => new Date(item));
    let calendar = new Calendar(".calendar_container", listDate);
    calendar.onclickDay = clickCalendarDay;
    calendar.createCalendar();

}


function clickCalendarDay(event) {
    var date = event.target.getAttribute("data-date");
    //var specialist_id = event.target.getAttribute("data-id");
    //console.log(date);

    let specialist = JSON.parse(localStorage.getItem("specialist"));
    getTimeSlotBySpecialistIdAndDate(specialist.specialist_id, date, false, showTimeSlot);

    //var showError = this.showError.bind(this);

}

function showTimeSlot(listTimeslot) {
    var main_container = document.querySelector(".time_slot_container");
    main_container.innerHTML = "";
    var timeslot = new ListTimeslot(".time_slot_container", listTimeslot);
    //timeslot.onClickTimeslot =  clickTimeslot.bind();
    timeslot.showList();
}


//код функции отображения психолога в личном кабинете психолога
function showSpecialist(data) {

    //код кнопки "выход пользователя"

    let containerButtonLogout = document.createElement('div');
    containerButtonLogout.classList.add('position-relative');

    let containerButtonLogout_2 = document.createElement('div');
    containerButtonLogout_2.classList.add("position-absolute", "top-0", "end-0", "translate-end");

    document.body.append(containerButtonLogout);
    containerButtonLogout.append(containerButtonLogout_2);

    let buttonLog = document.createElement('button');
    buttonLog.classList.add("btn", "btn-primary", "position-relative");
    containerButtonLogout_2.appendChild(buttonLog);
    buttonLog.append("Выход пользователя")


    buttonLog.onclick = function () {
        logOut();
        return false;
    }


    //контейнеры с боксом психолога
    let container = document.createElement('div');
    container.classList.add('container');

    let row = document.createElement("div");
    row.classList.add("row");

    document.body.append(container);
    container.append(row);

    let col = document.createElement('div');
    col.classList.add("col-10", "col-md-6", "offset-1", "offset-md-3");
    row.appendChild(col);

    let container_2 = document.createElement('div');
    container_2.classList.add("bg-info", "rounded", "p-3", "m-4");
    col.appendChild(container_2)

    let container_3 = document.createElement('div');
    container_3.classList.add("row", "align-items-center", "justify-content-center");
    container_2.appendChild(container_3)

    let col_2 = document.createElement('div');
    col_2.classList.add("col", "d-flex", "align-items-center", "justify-content-center");
    container_3.appendChild(col_2)

    let col_3 = document.createElement('div');
    col_3.classList.add("col", "d-flex", "align-items-start", "justify-content-start");
    container_3.appendChild(col_3);

    let h3 = document.createElement("h3");
    h3.innerHTML = data.name;

    let img = document.createElement("img");
    img.src = data.photo;
    img.style.height = "100px";
    img.style.width = "100px";
    img.style.borderRadius = "50%";


    col_2.append(img);
    col_3.appendChild(h3);

    //контейнер с боксом календаря

    let calendar_container = document.createElement('div');
    calendar_container.classList.add("calendar_container");
    document.body.appendChild(calendar_container);

    getCalendarSpecialist(data.specialist_id, false);

//контейнер с боксом открытых таймслотов
    let time_slot_container = document.createElement('div');
    time_slot_container.classList.add("time_slot_container");
    document.body.appendChild(time_slot_container);    


    //контейнер с кнопкой "добавить тайм-слот"
    let containerButtonDeleteTimeSlot = document.createElement('div');
    containerButtonDeleteTimeSlot.classList.add("container", "px-2");

    let containerButtonDeleteTimeSlot_2 = document.createElement('div');
    containerButtonDeleteTimeSlot_2.classList.add("row", "gx-2");

    let containerButtonDeleteTimeSlot_3 = document.createElement('div');
    containerButtonDeleteTimeSlot_3.classList.add("col-md-2", "mx-auto");

    let containerButtonDeleteTimeSlot_4 = document.createElement('div');
    containerButtonDeleteTimeSlot_4.classList.add("p-2", "bg-light");

    document.body.append(containerButtonDeleteTimeSlot);
    containerButtonDeleteTimeSlot.append(containerButtonDeleteTimeSlot_2);
    containerButtonDeleteTimeSlot_2.append(containerButtonDeleteTimeSlot_3);
    containerButtonDeleteTimeSlot_3.append(containerButtonDeleteTimeSlot_4);


    let buttonLogDeleteTimeslot = document.createElement('button');
    buttonLogDeleteTimeslot.classList.add("btn", "btn-primary");
    containerButtonDeleteTimeSlot_2.appendChild(buttonLogDeleteTimeslot);
    buttonLogDeleteTimeslot.append("добавить тайм-слот")

    buttonLogDeleteTimeslot.onclick = function () { 
        createTimeSlot();
        return false;
    }



    

    //контейнер с кнопкой "удалить тайм-слот"
    //  let containerButtonAddTimeSlot = document.createElement('div');
    //  containerButtonAddTimeSlot.classList.add("container", "px-4");

    //  let containerButtonAddTimeSlot_2 = document.createElement('div');
    //  containerButtonAddTimeSlot_2.classList.add("row", "gx-2");

    //  let containerButtonAddTimeSlot_3 = document.createElement('div');
    //  containerButtonAddTimeSlot_3.classList.add("col-md-6", "mx-auto");

    //  let containerButtonAddTimeSlot_4 = document.createElement('div');
    //  containerButtonAddTimeSlot_4.classList.add("p-2", "bg-light");

    //  document.body.append(containerButtonAddTimeSlot);
    //  containerButtonAddTimeSlot.append(containerButtonAddTimeSlot_2);
    //  containerButtonAddTimeSlot_2.append(containerButtonAddTimeSlot_3);
    //  containerButtonAddTimeSlot_3.append(containerButtonAddTimeSlot_4);


    //   let buttonLogAddTimeslot = document.createElement('button');
    //   buttonLogAddTimeslot.classList.add("btn", "btn-primary");
    //   containerButtonDeleteTimeSlot_2.appendChild(buttonLogAddTimeslot);
    //   buttonLogAddTimeslot.append("Удалить тайм-слот")

    //   buttonLogAddTimeslot.onclick = function () {
    //       logOut();
    //       return false;
    //   }

    //контейнер с таблицей записей
    let containerTableTimeSlot = document.createElement('div');
    containerTableTimeSlot.classList.add("container", "px-4");

    
    
    let tableTimeSlot = document.createElement('table');
    tableTimeSlot.classList.add("table", "table-bordered", "table-dark");
    let thead = document.createElement("thead");

    let tR = document.createElement('tr');    


    document.body.append(containerTableTimeSlot);
    containerTableTimeSlot.append(tableTimeSlot);
    tableTimeSlot.append(thead);
    thead.append(tR);
    ["Выбор", "Дата", "Время", "Имя", "Телефон", "Онлайн (да/не)"].forEach(item=>{
        let th = document.createElement("th");
        th.append(item);
        tR.append(th);
    })
    











}







