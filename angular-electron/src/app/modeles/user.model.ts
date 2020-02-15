import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class User {
    constructor(login: String, password: String, uploadTarget: String){
        this.login = login;
        this.password = password;
        this.uploadTarget = uploadTarget;
    }

    login: String;
    password: String;
    uploadTarget: String;
}