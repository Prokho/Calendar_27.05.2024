function ListTimeslot(selector, listData)
{
    this.selector = selector;
    this.main_container = document.querySelector(this.selector);
    this.listData = listData;
    this.onClickTimeslot = null;

    this.showList = function()
    {
        var oldCalendar = document.querySelector(".timeslots");
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
        this.timeslots = document.createElement("div");
        this.titel = document.createElement("div");
        this.titel.innerHTML = "Время для записи " + formatDateClassic(new Date(Date.parse(listData[0].date)));
        this.titel.classList.add("text-center", "mt-4", "mb-4", "larg-text");
        this.timeslots.classList.add("timeslots", "col-10", "col-md-6", "offset-1", "offset-md-3");
        this.timeslotsContainer = document.createElement("div");
        this.timeslotsRow = document.createElement("div");
        this.timeslotsContainer.classList.add("container-fluid");
        this.timeslotsRow.classList.add("row");

        this.timeslots.appendChild(this.titel);
        this.main_container.appendChild(this.timeslots);
        this.timeslots.appendChild(this.timeslotsContainer);
        this.timeslotsContainer.appendChild(this.timeslotsRow);

        this.listData.forEach(this.showItem.bind(this));

        this.timeslots.scrollIntoView();
    }

    this.showItem = function(timeslot)
    {
        var slot = document.createElement("div");
        slot.innerHTML = timeslot.time.split(':').slice(0, 2).join(':');
        slot.setAttribute("data-id", timeslot.id);
        var onClickTimeslot = this.onClickTimeslot;
        var timeslotsRow = this.timeslotsRow;
        slot.onclick = function(event)
        {
            onClickTimeslot(event);
            Array.from(timeslotsRow.children)
                .forEach(function(item){
                    item.classList.remove("bg-info");
                });

            event.target.classList.add("bg-info");
        } 
        slot.classList.add("col-2", "m-3", "text-center", "larg-text", "box-shadow", "pointer");

        this.timeslotsRow.appendChild(slot);
    }
}