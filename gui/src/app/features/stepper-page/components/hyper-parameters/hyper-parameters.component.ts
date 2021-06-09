import {Component} from '@angular/core';
import {BaseStepperSubFormComponent} from '../general-settings/base-stepper-sub-form-component';
import {Config} from '../../../../core/domain/models/full-config';
import {FormBuilder, FormControl, ValidationErrors, Validators} from '@angular/forms';
import {AdvancedHyperParameters} from '../../../../core/domain/models/hyperparemeters';
import {Observable, Observer} from 'rxjs';

@Component({
    selector: 'app-hyper-parameters',
    templateUrl: './hyper-parameters.component.html',
    styleUrls: ['./hyper-parameters.component.css']
})
export class HyperParametersComponent extends BaseStepperSubFormComponent {
    advancedChosen: boolean = false;

    constructor(private fb: FormBuilder) {
        super();
        // initializing defaults
        const config = new Config();
        this.form = this.fb.group({
            batch_size: [config.batch_size, [Validators.required], [this.checkIfIntValidator]],
            lr: [config.lr, [Validators.required]],
            epochs: [config.epochs, [Validators.required], [this.checkIfIntValidator]],
            validation_batch_size: [config.validation_batch_size, [Validators.required], [this.checkIfIntValidator]],
            momentum: [config.momentum, [Validators.required]],
            weight_decay: [config.weight_decay, [Validators.required]],
            num_workers: [config.num_workers, [Validators.required], [this.checkIfIntValidator]],
            crop_size: [config.crop_size, [Validators.required], [this.checkIfIntValidator]],
            base_size: [config.base_size, [Validators.required], [this.checkIfIntValidator]],
            augment_data: [config.augment_data, [Validators.required]],
        });
    }

    public checkIfIntValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            if (!String(control.value).match(/^[0-9]+$/)) {
                observer.next({error: true, notInt: true});
            } else {
                observer.next(null);
            }
            observer.complete();
        })

    public getFields(): AdvancedHyperParameters {
        this.form.patchValue({
            lr: Number(parseFloat(this.form.value.lr).toPrecision(4)),
            momentum: Number(parseFloat(this.form.value.momentum).toPrecision(4)),
            weight_decay: Number(parseFloat(this.form.value.lr).toPrecision(4))
        });
        return this.form.value;
    }

    public showAdvanced() {
        this.advancedChosen = !this.advancedChosen;
        if (!this.advancedChosen) {
            this.resetAdvancedFormValues();
        }
    }

    private resetAdvancedFormValues() {
        // put defaults back
        const {lr, batch_size, epochs, validation_batch_size, ...advanced} = new Config();
        this.form.patchValue({
            ...advanced
        });
        const advancedParams = Object.keys(advanced);
        Object.keys(this.form.controls)
            .filter(key => advancedParams.includes(key))
            .map(key => {
                this.form.controls[key].markAsUntouched();
                this.form.controls[key].markAsPristine();
            });
    }
}
