import {Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import * as fileSaver from 'file-saver';

@Component({
    selector: 'app-logs-modal',
    templateUrl: './logs-modal.component.html',
    styleUrls: ['./logs-modal.component.css']
})
export class LogsModalComponent implements OnInit, OnDestroy {
    @Input() modalSettings = {
        isVisible: false,
        specificLogsJobTitle: ''
    };
    @Input() data: string[];
    @Output() refresh: EventEmitter<void> = new EventEmitter<void>();
    private refreshInterval;

    constructor() {
        this.refresh = new EventEmitter<void>();
    }

    ngOnInit(): void {
        this.refreshInterval = setInterval(this.handleRefreshMiddle, 5000);
    }

    ngOnDestroy() {
        clearInterval(this.refreshInterval);
    }

    public hideModal() {
        this.modalSettings.isVisible = false;
    }

    public downloadLogs(): void {
        const downloadableData = this.data.join('\n');
        const blob = new Blob([downloadableData], {type: 'text/txt; charset=utf-8'});
        fileSaver.saveAs(blob, this.modalSettings.specificLogsJobTitle + '_logs ' + new Date().toDateString() + '.txt');
    }

    public handleRefreshMiddle = () => {
        if (this.refresh && this.modalSettings.isVisible) {
            const modal = document.querySelector('.ant-modal-body');
            modal.scroll({
                top: modal.scrollHeight,
                behavior: 'smooth'
            });
            this.refresh.emit();
        }
    }
}
