import { Directive, HostListener, HostBinding } from '@angular/core';

@Directive({
	selector: '[appDnd]'
})

export class DndDirective {

	//Une des properties de la balise hôte de la directive DND sera accessible dans celle-ci
	//Accessible avec this.quelquechose
	@HostBinding('style.background') private background = '#eee';

	constructor() { }

	//Déclarer des listener avec @Hostlistener
	//Quand on drag des fichiers
	@HostListener('dragover', ['$event']) onDragOver(evt){
		evt.preventDefault();
		evt.stopPropagation();
		let files = evt.dataTransfer.files;
		if(files.length > 0){
			this.background = '#999';
		}
	}
	
	//quand on arrête de drag
	@HostListener('dragleave', ['$event']) public onDragLeave(evt){
		evt.preventDefault();
		evt.stopPropagation();
		this.background = '#eee';
	}

	//quand on drop
	@HostListener('drop', ['$event']) public onDrop(evt){
		evt.preventDefault();
		evt.stopPropagation();
		let files = evt.dataTransfer.files;
		if(files.length > 0){
			this.background = '#eee';
		}
	}
}
