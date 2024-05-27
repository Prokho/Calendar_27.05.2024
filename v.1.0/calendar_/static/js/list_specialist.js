function ListSpecialist(selector, listSpecialist)
{
    this.onclickSpecialist = null;
    this.selector = selector;
    this.listSpecialist =  listSpecialist;
    this.main_container = document.querySelector(this.selector);

    this.showSpecialist=function()
    {
        this.specialist_conteiner = document.createElement("div");
        this.specialist_conteiner.classList.add("row");
        this.specialist_conteiner_col = document.createElement("div");
        this.specialist_conteiner_col.classList.add("col-10");
        this.specialist_conteiner_col.classList.add("col-md-6");
        this.specialist_conteiner_col.classList.add("offset-1");
        this.specialist_conteiner_col.classList.add("offset-md-3");
        this.specialist_list = document.createElement("ul");
        this.specialist_list.classList.add("p-0");
        this.specialist_list.classList.add("m-0");

        this.header = document.createElement("div");
        this.header.innerHTML = "Выберите специалиста для записи";
        this.header.classList.add("text-center");
        this.header.classList.add("h4");
        this.header.classList.add("mt-3");
        this.header.classList.add("mb-5");
        this.header.classList.add("bg-info");
        this.header.classList.add("rounded");
        this.header.classList.add("p-3");


        this.main_container.appendChild(this.specialist_conteiner);
        this.specialist_conteiner.appendChild(this.specialist_conteiner_col);
        this.specialist_conteiner_col.appendChild(this.header);
        this.specialist_conteiner_col.appendChild(this.specialist_list);

        this.listSpecialist.forEach(this.showItemListSpecialist.bind(this));
    }

    this.hideUnSelectedSpecialist = function(event)
    {
        var list = document.querySelectorAll(".specialist_item");
        var li = event.target.closest("li");
        list.forEach(function(item){
            if(item!= li)
            {
                item.remove();
            } 
        });
        li.onclick = function(){return false;}
        this.header.remove();
    }

    this.showItemListSpecialist = function(element)
    {
        let li = document.createElement("li");
        li.setAttribute("data-id", element.specialist_id);
        var action1 = this.onclickSpecialist;
        var action2 = this.hideUnSelectedSpecialist.bind(this);

        li.onclick = function(event)
        {
            action1(event);
            action2(event);
        }
        
        li.classList.add("specialist_item");
        li.classList.add("bg-info");
        li.classList.add("rounded");
        li.classList.add("p-1");
        li.classList.add("m-2");
        li.classList.add("pointer");

        var li_container = document.createElement("div");
        li_container.classList.add("container");

        var li_row = document.createElement("div");
        li_row.classList.add("row");
        
        

        var photo_col = document.createElement("div");
        var name_col = document.createElement("div");
        var photo = document.createElement("img");
        photo.src = element.photo;
        photo.style.height="70px";
        photo.style.width="70px";
        photo.style.borderRadius = "50%";


        photo_col.classList.add("col-md-3", "col-4");
        photo_col.classList.add("d-flex");

        name_col.classList.add("col-md-9", "col-8");
        name_col.classList.add("d-flex");

        li.appendChild(li_container);
        li_container.appendChild(li_row);
        photo_col.appendChild(photo);
        li_row.appendChild(photo_col);
        li_row.appendChild(name_col);


        name_col.innerHTML = '<div class="align-self-center">'+element.name+'</div>';

        this.specialist_list.appendChild(li);
    }
}