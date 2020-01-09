
import {Deserializable} from "./deserializeble.model";

export class File implements Deserializable {
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
