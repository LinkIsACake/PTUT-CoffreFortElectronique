import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class HomeService {
  private configUrl = 'http://localhost:8080/';

  constructor(private http: HttpClient) { }

  getHello() {
    return this.http.request('GET',this.configUrl, {responseType:'json'});
    //return this.http.get<any>(this.configUrl);
  }
}
