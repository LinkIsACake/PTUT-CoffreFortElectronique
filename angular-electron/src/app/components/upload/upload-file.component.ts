import {any} from "codelyzer/util/function";
import {Component} from "@angular/core";

@Component({
  selector: 'app-home',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})

class File{
  public name:String;
}

export class UploadComponent {
  files = [];

  uploadFile(event: Array<File>) {
    for (let index = 0; index < event.length; index++) {
      const element = event[index];
      this.files.push(element.name)
    }
  }

  deleteAttachment(index: any) {
    this.files.splice(index, 1)

  }
}
