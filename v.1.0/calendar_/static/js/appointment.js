// файл записи клиента
// он выводит информацию о записи - это финальная запись о том что клиент записан!!!


function Appointment(selector, appointmet)
{
    this.selector = selector;
    this.main_container = document.querySelector(this.selector);
    this.appointmet = appointmet;

    this.show = function()
    {
        var divAppointment = document.createElement("div");
        divAppointment.classList.add("col-10", "col-md-6", "offset-1", "offset-md-3");
        
        var divAppointmentContainer = document.createElement("div");
        divAppointmentContainer.classList.add("container-fluid", "mt-5");
        
        var divSuccessText = document.createElement("div");
        divSuccessText.classList.add("row");
        var divSpecialist = document.createElement("div");
        divSpecialist.classList.add("row");
        var divDate = document.createElement("div");
        divDate.classList.add("row");
        var divTime = document.createElement("div");
        divTime.classList.add("row");


        if(this.appointmet.hasOwnProperty('error'))
        {
            var divError = document.createElement("div");
            divError.innerHTML="Возникла ошибка обновите страницу и попробуйте еще раз";
            this.main_container.appendChild(divError);
        }
        else
        {
            divSuccessText.innerHTML = "Вы записаны на прием";
            console.log(this.appointmet)
            if(!this.appointmet.time_slot.online)
            {
                divSuccessText.innerHTML += " г. Москва, ул. Орджоникидзе, д.11, стр. 11, 2 этаж, офис 201";
            }
            else
            {
                divSuccessText.innerHTML += " ОНЛАЙН";
            }
            divDate.innerHTML = "Дата приема: "+ this.appointmet.time_slot.date;
            divTime.innerHTML = "Время приема: "+ this.appointmet.time_slot.time.split(':').slice(0, 2).join(':');
            divSpecialist.innerHTML = "Ваш специалист "+ this.appointmet.time_slot.user.name;
        

                
            divAppointmentContainer.appendChild(divSuccessText);
            divAppointmentContainer.appendChild(divDate);
            divAppointmentContainer.appendChild(divTime);
            divAppointmentContainer.appendChild(divSpecialist);



            divAppointment.appendChild(divAppointmentContainer);
            this.main_container.appendChild(divAppointment);
        }

    }
}