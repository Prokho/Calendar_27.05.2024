function API()
{

    this.getListSpecialist = function(successHandler, failHandler)
    {
        let response = fetch("/specialist/");
        response.then(r => this.processResponse(r, successHandler, failHandler));
    }

    this.getCalendarSpecialist = function(specialist_id, online, successHandler, failHandler)
    {
        let today = formatDate(new Date());
        let dayAfterThreeMonth = formatDate(new Date(new Date().setDate(new Date().getDate() + 90)));
        let body = {"begin": today, "end": dayAfterThreeMonth, "specialist_id": specialist_id, "online": online};
        let bodyJSON = JSON.stringify(body);
        let response = fetch('/get_freedate_list/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json;charset=utf-8'},
            body: bodyJSON
        });
        response.then(r => this.processResponse(r, successHandler, failHandler));
    }

    this.processResponse = function(response, successHandler, failHandler)
    {
        if(!response.ok){
            failHandler(response.status);
        }
        else{
            response.json().then(successHandler);
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
// function API()
// {

//     this.getListSpecialist = function(successHandler, failHandler)
//     {
//         let response = fetch("/specialist/");
//         response.then(r => this.processResponse(r, successHandler, failHandler));
//     }

//     this.showCalendarSpecialist = function(specialist_id, successHandler, failHandler)
//     {
//         let today = new Date().toLocaleDateString('en-CA');
//         let dayAfterThreeMonth = new Date(new Date().setDate(new Date().getDate() + 90)).toLocaleDateString("en-CA");
//         let body = {"begin": today, "end": dayAfterThreeMonth, "specialist_id": specialist_id};
//         let bodyJSON = JSON.stringify(body);
//         let response = fetch('/get_freedate_list/', {
//             method: 'POST',
//             headers: {'Content-Type': 'application/json;charset=utf-8'},
//             body: bodyJSON
//         });
//         response.then(r => processResponse(r, successHandler, failHandler));
//     }

//     this.processResponse = function(response, successHandler, failHandler)
//     {
//         if(!response.ok){
//             failHandler(response.status);
//         }
//         else{
//             response.json().then(successHandler);
//         }
//     }
// }