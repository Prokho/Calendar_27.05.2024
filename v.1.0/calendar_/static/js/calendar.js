// календарь

function formatDate(date = new Date()) {
    const year = date.toLocaleString('default', {year: 'numeric'});
    const month = date.toLocaleString('default', {month: '2-digit'});
    const day = date.toLocaleString('default', {day: '2-digit'});

    return [year, month, day].join('-');
}

function formatDateClassic(date = new Date()) {
    const year = date.toLocaleString('default', {year: 'numeric'});
    const month = date.toLocaleString('default', {month: '2-digit'});
    const day = date.toLocaleString('default', {day: '2-digit'});

    return [day, month, year].join('.');
}

function Calendar(selector, listDate){
    this.onclickDay = null;
    this.selector = selector;
    this.listDate =  listDate;
    this.monthNames =  [
        "Январь", "Февраль", "Март", "Апрель", "Май", 
        "Июнь", "Июль", "Август", "Сентябрь", 
        "Октябрь", "Ноябрь", "Декабрь"
    ];
    this.offset = 0;

    this.createCalendar = function()
    {
        this.container = document.querySelector(this.selector);

        var oldCalendar = document.querySelector(".calendar-container");
        if(oldCalendar)
        {
            var element = oldCalendar
            while(element)
            {
                var nextNode = element.nextSibling;
                element.remove();
                element = nextNode;
            }
        }

        var row = document.createElement("div");
        row.classList.add("row", "calendar-container", "mt-5");
        var calendar_col = document.createElement("div");
        calendar_col.classList.add("col-10");
        calendar_col.classList.add("col-md-6");
        calendar_col.classList.add("offset-1");
        calendar_col.classList.add("offset-md-3");


        this.calendar = document.createElement("div");
        this.div_header = document.createElement("div");
        this.header = document.createElement("h1");
        this.right = document.createElement("div");
        this.left = document.createElement("div");
        this.calendar__date = document.createElement("div");

        this.calendar.classList.add("calendar");
        this.div_header.classList.add("header");
        this.right.classList.add("right");
        this.left.classList.add("left");
        this.calendar__date.classList.add("calendar__date");


        this.container.appendChild(row);
        row.appendChild(calendar_col);
        calendar_col.appendChild(this.calendar);
        this.calendar.appendChild(this.div_header);
        this.div_header.appendChild(this.header);
        this.div_header.appendChild(this.right);
        this.div_header.appendChild(this.left);
        this.calendar.appendChild(this.calendar__date);


        this.right.onclick=()=>{
            this.offset++;
            this.showCalendar();
        }

        this.left.onclick=()=>{
            this.offset--;
            this.showCalendar();
        }

        this.showCalendar();
    }

    this.containsDate = function(date)
    {
        return this.listDate.filter(
            item=> item.getFullYear() ==  date.getFullYear() &&
            item.getMonth() == date.getMonth() &&
            item.getDate() == date.getDate()
        ).length !=0;
    }

    this.firstDayForMonth = function(date)
    {
        let curDay = date.getDate();
        let curWeekDay = (date.getDay()+6)%7;
        firstWeekDay = curWeekDay;
        for(let i = 0; i<curDay-1; i++)
        {
            firstWeekDay--;
            if(firstWeekDay<0)
            {
                firstWeekDay=6;
            }
        }
        return firstWeekDay;
    }

    this.showCalendar = function()
    {
        let curData = new Date();
        let year = curData.getYear();
        let curMonth =  curData.getMonth()
        let month = curMonth+this.offset;
        let curDay = curData.getDate();

        let dateWithOffset = new Date(curData.getFullYear(), month, curDay);

        let lastDate = new Date(year, month+1, 0);
        let lastDay = lastDate.getDate();
        let firstDay = this.firstDayForMonth(dateWithOffset);


        this.header.innerHTML = this.monthNames[dateWithOffset.getMonth()] + " " + dateWithOffset.getFullYear();

        this.calendar__date.innerHTML = "";
        this.calendar__date.innerHTML+=`<div class="calendar__day">ПН</div>
        <div class="calendar__day">ВТ</div>
        <div class="calendar__day">СР</div>
        <div class="calendar__day">ЧТ</div>
        <div class="calendar__day">ПТ</div>
        <div class="calendar__day">СБ</div>
        <div class="calendar__day">ВС</div>`
        
        for(let i=0; i < firstDay; i++)
        {
            this.calendar__date.innerHTML += '<div class="calendar__number"></div>';
        }

        for(let i=1; i <=lastDay; i++)
        {
            let date = new Date(curData.getFullYear(), month, i)
            let divDay = document.createElement('div');
            divDay.classList.add("calendar__number");
            if(this.offset==0 && i==curDay)
            {
                divDay.classList.add("calendar__number--current");
            }
            if(this.containsDate(date) && date.getTime()>=new Date(curData.getFullYear(), curMonth, curDay).getTime())
            {
                divDay.classList.add("calendar_open_time_slot");
                divDay.setAttribute("data-date", formatDate(date))
                divDay.onclick = this.onclickDay;
            }
            divDay.innerHTML = i;
            this.calendar__date.appendChild(divDay);
        }

        this.calendar.scrollIntoView();
    }
}