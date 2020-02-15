import { Component, OnInit } from '@angular/core';
import {HomeService} from "../../services/home.service";
import {File} from "../../modeles/file.model"
import { UploadComponent} from "../upload/upload-file.component";
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent implements OnInit {

  private fileList : File[];
  private fileDetail : File;

  constructor(private homeService : HomeService,public matDialog: MatDialog) {

    this.fileList = []
    this.homeService.readFolder()
      .subscribe((data: Array<String>) => {
        data.forEach(file => {
          this.homeService.readFile(file).subscribe((data : File) => {
            data.name = file;
            this.fileList.push(data);
          })
        })
      })


  }

  ngOnInit() {

  }

  FileDetail(name: String)  {
    this.homeService.readFile(name)
      .subscribe((data : File) => {
        this.fileDetail = data;
        this.fileDetail.name = name;
      });
  }

  
  openUpload() {
    const uploadConfig = new MatDialogConfig();
    uploadConfig.id = "upload-file-component";
    uploadConfig.height = "350px";
    uploadConfig.width = "600px";
    const modalDialog = this.matDialog.open(UploadComponent, uploadConfig);
  }
}
