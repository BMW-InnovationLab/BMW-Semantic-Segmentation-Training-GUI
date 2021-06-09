import {Component, Input} from '@angular/core';

@Component({
    selector: 'app-advanced-parameters',
    templateUrl: './advanced-parameters.component.html',
    styleUrls: ['./advanced-parameters.component.css']
})
export class AdvancedParametersComponent {
    @Input() public form;
}
