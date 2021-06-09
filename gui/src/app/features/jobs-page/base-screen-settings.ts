export class BaseScreenSettings {
    public mobile: boolean;
    public windowHeightSmall: boolean;

    constructor() {
        this.initializeScreenSettings();
    }

    private initializeScreenSettings() {
        this.mobile = window.screen.width <= 1024;
        this.windowHeightSmall = window.screen.height < 710;
        window.onresize = () => {
            this.mobile = window.screen.width <= 1024;
            this.windowHeightSmall = window.screen.height < 710;
        };
    }
}
