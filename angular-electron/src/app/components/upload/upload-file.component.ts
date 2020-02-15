import {any} from "codelyzer/util/function";
import {Component} from "@angular/core";

@Component({
  selector: 'app-home',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})

export class UploadComponent {
  files = [];

  uploadFile(event: Event) {
    for (let index = 0; index < 5; index++) {
      const element = event[index];
      this.files.push(element.name)
    }
  }

  deleteAttachment(index: any) {
    this.files.splice(index, 1)

  }
}
