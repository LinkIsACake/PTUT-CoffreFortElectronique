import { Component, OnInit } from '@angular/core';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit  {

  constructor() { }

  ngOnInit() {
  }

	onSubmit(form: NgForm) {
	    console.log("Valeurs entrées: "+form.value);
			const login = form.value['login'];
			const passwd = form.value['password'];
	}
}
