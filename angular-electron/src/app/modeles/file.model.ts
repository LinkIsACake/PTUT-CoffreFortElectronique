
import {Deserializable} from "./deserializeble.model";

export class File implements Deserializable {

  constructor(name: string) {
    File.size+=1;
    this.name = name
    this.id = File.size
  }

  static size = 0;

  id: number;
  name: String;
  uid: String;
  gid: String;
  size: String;
  birthtime: String;


  deserialize(input: any): this {
    Object.assign(this,input);
    return this;
  }


}
