function TypeAppointment(selector)
{
    this.onclickButton = null;
    this.selector = selector;
    this.main_container = document.querySelector(this.selector);

    this.showButtons=function()
    {
        this.button_conteiner = document.createElement("div");
        this.button_conteiner.classList.add("row", "mt-5");

        this.button_conteiner_col_left = document.createElement("div");
        this.button_conteiner_col_left.classList.add("col-5", "offset-1", "text-center");

        
        this.button_conteiner_col_right = document.createElement("div");
        this.button_conteiner_col_right.classList.add("col-5", "text-center");

        this.button_online = document.createElement("button");
        this.button_offline = document.createElement("button");

        this.button_online.classList.add("w-75", "btn", "btn-info");
        this.button_offline.classList.add("w-75", "btn", "btn-info");

        this.button_online.value = "true";
        this.button_offline.value = "false";


        this.button_online.innerHTML = "online";
        this.button_offline.innerHTML = "в кабинете";


        this.main_container.appendChild(this.button_conteiner);
        this.button_conteiner.appendChild(this.button_conteiner_col_left);
        this.button_conteiner.appendChild(this.button_conteiner_col_right);

        this.button_conteiner_col_left.appendChild(this.button_online);
        this.button_conteiner_col_right.appendChild(this.button_offline);

        this.button_online.onclick = this.onclickButton;
        this.button_offline.onclick = this.onclickButton;
    }
}