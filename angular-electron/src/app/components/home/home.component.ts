import { Component, OnInit } from '@angular/core';
import {HomeService} from "../../services/home.service";

export interface Response {
  textfile: string;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {

  private fileList : String[];

  constructor(private homeService :HomeService) {
    this.fileList = []
    this.homeService.getHello()
      .subscribe((data: Array<String>) => {
        data.forEach(file => this.fileList.push(file))
      });

  }

  ngOnInit() {

  }

}
