import {Component, Input} from '@angular/core';

@Component({
    selector: 'app-basic-parameters',
    templateUrl: './basic-parameters.component.html',
    styleUrls: ['./basic-parameters.component.css']
})
export class BasicParametersComponent {
    @Input() public form;
}
