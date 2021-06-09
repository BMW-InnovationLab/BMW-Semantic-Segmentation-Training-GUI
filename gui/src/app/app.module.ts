import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {en_US, NZ_I18N} from 'ng-zorro-antd/i18n';
import {registerLocaleData} from '@angular/common';
import en from '@angular/common/locales/en';
import {NzPageHeaderModule} from 'ng-zorro-antd/page-header';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzIconModule} from 'ng-zorro-antd/icon';
import { NzBadgeModule } from 'ng-zorro-antd/badge';
import { NzCardModule} from 'ng-zorro-antd/card';
import { NzListModule} from 'ng-zorro-antd/list';
import { NzDividerModule} from 'ng-zorro-antd/divider';
import { NzEmptyModule} from 'ng-zorro-antd/empty';
import { NzFormModule} from 'ng-zorro-antd/form';
import { NzGridModule} from 'ng-zorro-antd/grid';
import { NzInputModule} from 'ng-zorro-antd/input';
import { NzInputNumberModule} from 'ng-zorro-antd/input-number';
import { NzLayoutModule} from 'ng-zorro-antd/layout';
import { NzModalModule} from 'ng-zorro-antd/modal';
import { NzPaginationModule} from 'ng-zorro-antd/pagination';
import { NzPopconfirmModule} from 'ng-zorro-antd/popconfirm';
import { NzPopoverModule} from 'ng-zorro-antd/popover';
import { NzStepsModule} from 'ng-zorro-antd/steps';
import { NzToolTipModule} from 'ng-zorro-antd/tooltip';
import {NzMessageModule} from 'ng-zorro-antd/message';
import {NzAlertModule} from 'ng-zorro-antd/alert';
import {NzSelectModule} from 'ng-zorro-antd/select';
import {NzDropDownModule} from 'ng-zorro-antd/dropdown';
import {NzTagModule} from 'ng-zorro-antd/tag';
import {NzTreeSelectModule} from 'ng-zorro-antd/tree-select';
import {NzSwitchModule} from 'ng-zorro-antd/switch';

import { NzConfig, NZ_CONFIG } from 'ng-zorro-antd/core/config';
import {ScrollingModule} from '@angular/cdk/scrolling';
import {ErrorHandler} from './core/interceptors/error-handler';
import {LandingPageComponent} from './core/components/landing-page/landing-page.component';
import {HeaderComponent} from './shared/components/header/header.component';
import {HyperParametersComponent} from './features/stepper-page/components/hyper-parameters/hyper-parameters.component';
import {GeneralSettingsComponent} from './features/stepper-page/components/general-settings/general-settings.component';
import {PrepareDatasetComponent} from './features/stepper-page/components/prepare-dataset/prepare-dataset.component';
import {StepperPageComponent} from './features/stepper-page/stepper-page.component';
import {JobsPageComponent} from './features/jobs-page/jobs-page.component';
import { JobItemComponent } from './features/jobs-page/components/job-item/job-item.component';
import { LogsModalComponent } from './features/jobs-page/components/logs-modal/logs-modal.component';
import {NotFoundComponent} from './core/components/not-found/not-found.component';
import { NetworksBackboneOptionComponent } from './features/stepper-page/components/general-settings/components/networks-backbone-option/networks-backbone-option.component';
import { PreTrainedOfflineAndCheckpointOptionComponent } from './features/stepper-page/components/general-settings/components/pre-trained-offline-and-checkpoint-option.component/pre-trained-offline-and-checkpoint-option.component';
import { ClassifierWeightOptionComponent } from './features/stepper-page/components/general-settings/components/classifier-weight-option/classifier-weight-option.component';
import { PreTrainedNetworkWeightsComponent } from './features/stepper-page/components/general-settings/components/pre-trained-network-weights/pre-trained-network-weights.component';
import {BasicParametersComponent} from './features/stepper-page/components/hyper-parameters/components/basic-parameters/basic-parameters.component';
import {AdvancedParametersComponent} from './features/stepper-page/components/hyper-parameters/components/advanced-parameters/advanced-parameters.component';
import {NzCheckboxModule} from 'ng-zorro-antd/checkbox';

const ngZorroConfig: NzConfig = {
    message: { nzDuration: 4000 },
};

registerLocaleData(en);


@NgModule({
    declarations: [
        AppComponent,
        LandingPageComponent,
        JobsPageComponent,
        StepperPageComponent,
        PrepareDatasetComponent,
        GeneralSettingsComponent,
        HyperParametersComponent,
        HeaderComponent,
        JobItemComponent,
        LogsModalComponent,
        NotFoundComponent,
        NetworksBackboneOptionComponent,
        PreTrainedOfflineAndCheckpointOptionComponent,
        ClassifierWeightOptionComponent,
        PreTrainedNetworkWeightsComponent,
        BasicParametersComponent,
        AdvancedParametersComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        HttpClientModule,
        BrowserAnimationsModule,
        NzPageHeaderModule,
        NzButtonModule,
        NzIconModule,
        NzDividerModule,
        NzPopoverModule,
        NzEmptyModule,
        NzGridModule,
        NzCardModule,
        NzListModule,
        NzPaginationModule,
        NzPopconfirmModule,
        NzLayoutModule,
        NzStepsModule,
        ReactiveFormsModule,
        NzFormModule,
        NzInputModule,
        NzSelectModule,
        NzInputNumberModule,
        NzAlertModule,
        NzToolTipModule,
        NzBadgeModule,
        NzModalModule,
        ScrollingModule,
        NzMessageModule,
        NzDropDownModule,
        NzTagModule,
        NzTreeSelectModule,
        NzSwitchModule,
        NzCheckboxModule,
    ],
    providers: [
        {
            provide: NZ_I18N, useValue: en_US
        },
        {
            provide: HTTP_INTERCEPTORS,
            useClass: ErrorHandler,
            multi: true
        },
        { provide: NZ_CONFIG, useValue: ngZorroConfig }
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
