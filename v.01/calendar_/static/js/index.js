// основной файл, который связывает все остальные файлы


function Controler(base_selector)// функция создает обьект контроллер (так как все связывает), сдесь функция создает обьект по аналогии с классом в других языках
// - base_selector - параметр
{
    this.base_selector = base_selector;// this.base_selector - создали атрибут для дальнейшего использования, это поле которое будет хранить селектор и отдавать его тем функциям который им будет нужен, селектор - это последовательность символов позволяющая отличить один элемент от другого
    this.api = new API();//создание обьекта по существующей функции в другом файле. Импорт происходит через хтмл файл.
    this.specialistId = null;// обьявление переменной, this нужно для обозначентя области видимости этой переменной, она будет работать на уровне обьекта.
    this.start = function() // this - это ссылка на текущий обьект, .start - это имя атрибута, = значит чему этот атрибут равен, а равен он функции, которая находиться в фигурных скобках {}
    // смотри https://learn.javascript.ru/object-methods
    // по сути в джава мы бы присвоили название функции start. По смыслу было бы то же самое
    {
        document.querySelector(this.base_selector).innerHTML="";
        var showListSpecialist = this.showListSpecialist.bind(this);
        // showListSpecialist - функция обьявленная ниже, мы привязали эту функцию к текущему обьекту через bind
        var showError = this.showError.bind(this);//то же самое с другой функцией
        this.api.getListSpecialist(showListSpecialist, showError)
        //передаем функцию getListSpecialist ссылки на функции showListSpecialist, showError
        // getListSpecialist  обьявлено внутри обьекта ей пи ай, смотри файл ей пи ай
        // смысл - вызов функции getListSpecialist, так как функция возвращает список специалистов, с которым мы дальше работаем.
    }

    this.showError = function(error)
    {
        let main_container = document.querySelector(this.base_selector); // document - готовая переменная в js - почитать про нее
        let div_error = document.createElement("div");// создали элемент(контейнер) для дальнейшего использования и вызова
        //createElement - эта функция обьявлена в самом языке.
        div_error.innerHTML = "что-то пошло не так, попробуйте позже";
        // здесь конструкция нужна для того чтобы вложить элемент - текст с помощью .innerHTML
        main_container.appendChild(div_error); // div_error вставляется внутрь другого элемента
    }

    this.showListSpecialist = function(list)
    {
        let main_container = document.querySelector(this.base_selector); 
        main_container.innerHTML="";
        let listSpecialist = new ListSpecialist(this.base_selector, list);
        listSpecialist.onclickSpecialist = this.clickSpecialist.bind(this);
        listSpecialist.showSpecialist();
    }

    this.clickSpecialist = function(event)
    {
        let target = event.target;
        let specialist_id = target.closest('li').getAttribute("data-id");
        this.specialistId = specialist_id;
        window.history.pushState(null, null, "#calendar");
        this.showTypeAppointment();
        return false;
    }

    this.showTypeAppointment = function()
    {
        var typeAppointment = new TypeAppointment(this.base_selector);
        typeAppointment.onclickButton = this.clickTypeAppointment.bind(this);
        typeAppointment.showButtons();
    }

    this.clickTypeAppointment = function(event)
    {
        let target = event.target;
        this.online = JSON.parse(target.value);
        this.showCalendarSpecialist();
        return false;
    }

    this.showCalendarSpecialist = function()
    {
        var showCalendar = this.showCalendar.bind(this);
        var showError = this.showError.bind(this);
        this.api.getCalendarSpecialist(this.specialistId, this.online, showCalendar, showError);
    }

    this.showCalendar = function(listDate){
        listDate = listDate.map(item => new Date(item));
        let calendar = new Calendar(this.base_selector, listDate);
        calendar.onclickDay = this.clickCalendarDay.bind(this);
        calendar.createCalendar();
    }

    this.clickCalendarDay = function(event){
        var date = event.target.getAttribute("data-date");
        var showTimeslot = this.showTimeslot.bind(this);
        var showError = this.showError.bind(this);
        this.api.getTimeSlotBySpecialistIdAndDate(this.specialistId, date, this.online, showTimeslot, showError);
    }

    this.showTimeslot = function(listTimeslot){
        var timeslot = new ListTimeslot(this.base_selector, listTimeslot);
        timeslot.onClickTimeslot =  this.clickTimeslot.bind(this);
        timeslot.showList();
    }

    this.clickTimeslot = function(event)
    {
        var target = event.target;
        var timeslotId = target.getAttribute("data-id");
        var appointment = new AppointmentSignUp(this.base_selector, timeslotId);
        appointment.showError = this.showError.bind(this);
        appointment.showApointment = this.showApointment.bind(this);
        appointment.validatePhone = this.api.validatePhone.bind(this.api);
        appointment.signUp = this.api.apointmentSignUp.bind(this.api);
        appointment.showForm();
    }

    this.showApointment = function(apointment)
    {
        this.main_container = document.querySelector(this.base_selector);
        this.main_container.innerHTML = "";
        var appointment = new Appointment(this.base_selector, apointment);
        appointment.show();
    }
}






