import {FormGroup} from '@angular/forms';

export abstract class BaseStepperSubFormComponent {
    public form: FormGroup;
    public abstract getFields();

    public isValid(): boolean {
        Object.keys(this.form.controls).forEach(key => {
            this.form.controls[key].markAsDirty();
            this.form.controls[key].updateValueAndValidity();
        });
        return this.form.valid;
    }
}
