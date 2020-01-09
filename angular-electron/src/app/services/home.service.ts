import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {File} from "../modeles/file.model";
import {Observable} from "rxjs";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})

export class HomeService {
  private configUrl = 'http://localhost:8080/';



  constructor(private http: HttpClient) { }

  readFolder() {
    return this.http.request('GET',this.configUrl + "readFolder", {responseType:'json'});
  }

  readFile(name : String) : Observable<File> {
    let res = this.http.get(this.configUrl + "readFile" + '/' + name);
    let object = res.pipe(map((res:Response) =>  new File().deserialize(res)));
    return object;
  }
}
