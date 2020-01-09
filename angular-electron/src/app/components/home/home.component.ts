import { Component, OnInit } from '@angular/core';
import {HomeService} from "../../services/home.service";
import {File} from "../../modeles/file.model"

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {

  private fileList : String[];
  private fileDetail : File;

  constructor(private homeService :HomeService) {
    this.fileList = []
    this.homeService.readFolder()
      .subscribe((data: Array<String>) => {
        data.forEach(file => this.fileList.push(file))
      });


  }

  ngOnInit() {

  }

  FileDetail(name: String){
    this.homeService.readFile(name)
      .subscribe((data : File) => {
        this.fileDetail = data;
        this.fileDetail.name = name;
      });
  }

}
