// форма для заполнения клиентом номера телефона и валидация номера телефона
// в файле нужно сделать проверку на то, что все поля не пустые
// при нажатие на кнопку "получит код" должен быть заполнен номер телефона как минимум
// по хорошему имя тоже должно быть заполнено
// посмотреть как сделан дизайн вывода кнопки и поля внесения кода


function AppointmentSignUp(selector, timeslotId)
{
    this.selector = selector;
    this.main_container = document.querySelector(this.selector);
    this.timeslotId = timeslotId;
    this.signUp = null;
    this.validatePhone = null;
    this.showApointment = null;
    this.showError = null;

    this.showForm = function()
    {
        var oldCalendar = document.querySelector(".signUp");
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

        var formRow = document.createElement("div");
        var formCol = document.createElement("div");
        var formContainer = document.createElement("div");

        formRow.classList.add("signUp", "row", "mt-4");
        formCol.classList.add("timeslots", "col-10", "col-md-6", "offset-1", "offset-md-3");
        formContainer.classList.add("container-fluid", "d-flex", "justify-content-center");


        
        var form = document.createElement("div");
        this.divPhone = document.createElement("div");
        var divName = document.createElement("div");
        this.divBtnCode = document.createElement("div");
        this.divBtnSignUp = document.createElement("div");
        var divCode = document.createElement("div");
        this.inputPhone = document.createElement("input");
        this.inputName = document.createElement("input");
        this.inputCode = document.createElement("input");
        this.btnCode = document.createElement("button");
        this.btnSignUp = document.createElement("button");
        this.btnCode.innerHTML = "Получить код";
        this.btnCode.onclick = this.onClickValidatePhone.bind(this);
        this.btnSignUp.innerHTML = "Записаться";
        this.btnSignUp.onclick = this.onClickSignUp.bind(this);

        this.inputPhone.placeholder = "Телефон";
        this.inputName.placeholder = "Имя";
        this.inputCode.placeholder = "Внесите код из СМС";
       
        this.divBtnCode.appendChild(this.btnCode);
        this.divBtnCode.classList.add("text-center");
        //this.divBtn.appendChild(this.btnSignUp);

        this.btnCode.classList.add("btn", "w-100", "btn-info", "mb-2");
        this.btnSignUp.classList.add("btn", "w-100", "btn-info");
        
        this.divPhone.appendChild(this.inputPhone);
        this.divPhone.classList.add("mb-2");
        divName.appendChild(this.inputName);
        divName.classList.add("mb-2");
        divCode.appendChild(this.inputCode);
        divCode.classList.add("mb-2");

        form.appendChild(this.divPhone);
        form.appendChild(divName);
        form.appendChild(divCode);
        form.appendChild(this.divBtnCode);
        form.appendChild(this.divBtnSignUp);
        form.classList.add("signUp");

        formRow.appendChild(formCol);
        formCol.appendChild(formContainer);
        formContainer.appendChild(form);

        this.main_container.appendChild(formRow);

        form.scrollIntoView();
    }

    this.showSignUpBtn = function(){
        this.divBtnSignUp.appendChild(this.btnSignUp);
        this.divBtnSignUp.scrollIntoView(false);
    }

    this.phonIsCorrect=function(phone)
    {
        return phone.length>=11;
    }

    this.codeIsCorrect=function(code)
    {
        if(/^\d+$/.test(code))
        {
            return code.length==4;
        }
        return false; 
    }

    this.nameIsCorrect=function(name)
    {
        return name.length>1;
    }

    this.phoneClean=function(phone)
    {
        var phone = phone.replace(/^\D+/g, '');
        if(phone.length>0 && phone[0]==8)
        {
            phone = "7" + phone.slice(1);
        } 
        else if (phone.length==10 && phone[0]==9)
        {
            phone = "7" + phone;
        }
        return phone;
    }

    this.onClickValidatePhone = function()
    {
        var phone = this.phoneClean(this.inputPhone.value);
        if(this.phonIsCorrect(phone))
        {
            this.inputPhone.classList.remove("border-danger");
            this.inputPhone.placeholder ="Телефон"; 
            var showSignUpBtn = this.showSignUpBtn.bind(this);
            this.validatePhone(phone, showSignUpBtn, this.showError);
            this.divBtnCode.innerHTML = "60 сек";
            var divTimet = this.divBtnCode;
            var btn = this.btnCode;
            var idIntreval = setInterval(function(){
                var val = parseInt(divTimet.innerHTML);
                divTimet.innerHTML = --val + " сек";
                if(val==0)
                {
                    divTimet.innerHTML="";
                    divTimet.appendChild(btn);
                    clearInterval(idIntreval);
                }
            }, 1000);

        }
        else
        {
            this.inputPhone.value="";
            this.inputPhone.placeholder ="Неверный номер"; 
            this.inputPhone.classList.add("border-danger");
            this.inputPhone.classList.add("rounded");
        }
    }

    this.onClickSignUp = function()
    {
        var error = false;
        var phone = this.phoneClean(this.inputPhone.value);
        var name = this.inputName.value.trim();
        var code = this.inputCode.value.replace(/^\D+/g, '');
        if(!this.phonIsCorrect(phone))
        {
            error=true;
            this.inputPhone.value="";
            this.inputPhone.placeholder ="Неверный номер"; 
            this.inputPhone.classList.add("border-danger");
            this.inputPhone.classList.add("rounded");
        }
        if(!this.codeIsCorrect(code))
        {
            error=true;
            this.inputCode.value="";
            this.inputCode.placeholder ="Неверный код"; 
            this.inputCode.classList.add("border-danger");
            this.inputCode.classList.add("rounded");
        }
        if(!this.nameIsCorrect(name))
        {
            error=true;
            this.inputName.value="";
            this.inputName.placeholder ="Неверное имя"; 
            this.inputName.classList.add("border-danger");
            this.inputName.classList.add("rounded");
        }
        if(!error)
        {
            var data = {
                phone: phone,
                timeslot_id: this.timeslotId,
                name: name,
                description: "empty",
                code_validation: code
            };
            this.signUp(data, this.showApointment, this.showError);
        }
    }
}
