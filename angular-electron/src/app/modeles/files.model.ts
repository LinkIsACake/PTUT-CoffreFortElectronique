import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class Files {
  constructor(name: String) {
        this.name = name;
  }
  name : String;

}
