function haptic_biofeedback()
clc;
delete(timerfindall);
delete(instrfindall);

%%%%%%%%%%%%%%%%%%%%%%    global   %%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%  Robert's setup   %%%%%%%%%%%%%%%%%%%
 bh_port = 'COM5';
% qs_port = 'COM4';
% haptic_port = 'COM6';
% accel_port = 'COM16';
% plot_time = 60;  %	how many seconds of data the plots display

%%%%%%%%%%%%%%%%%  Robert's setup  %%%%%%%%%%%%%%%%%%%
bh_remote_name = 'BH BHT022509';
%bh_port = '/dev/cu.BHBHT023730-iSerialPort1';
qs_port = '/dev/tty.AffectivaQ-v2-D9B8-SPP';
haptic_port = '/dev/tty.usbmodem1411';
accel_port = '/dev/tty.wchusbserial1420';
plot_time = 60;  %	how many seconds of data the plots display


% bioharness connection and packet stream
bh_conn=[];
bh_connected = 0;
ps=[];

% qsensor connection
qs_conn=[];
qs_connected = 0;

% haptic connection
haptic_conn = [];
haptic_connected = 0;

% accelerometer connection
accel_conn = [];
accel_connected = 0;


%%%%%%%%%%%%%%%%%%%%%%   timers %%%%%%%%%%%%%%%%%%%%%%%%%%%%
bh_timer = timer('TimerFcn', @read_bh_packets, ...
    'Period', 1, 'ExecutionMode', 'FixedRate');

qs_timer = timer('TimerFcn', @read_qs_data, ...
    'Period', .1, 'ExecutionMode', 'FixedRate');

accel_timer = timer('TimerFcn', @read_accel_data, ...
    'Period', .050, 'ExecutionMode', 'FixedRate');
    
heartbeat_timer = timer('TimerFcn', @play_heartbeat, ...
    'Period', 1, 'ExecutionMode', 'FixedRate');

breath_timer = timer('TimerFcn', @play_breath, ...
    'Period', 6, 'ExecutionMode', 'FixedRate');

sequential_timer = timer('TimerFcn', @play_sequential, ...
    'Period', 7, 'ExecutionMode', 'FixedRate');

sound_timer = timer('TimerFcn', @Bioharness_OUTPUT, ...
    'Period', 0.01, 'ExecutionMode', 'FixedRate');
%%%%%%%%%%%%%%%%%%%%%%%  bioharness data packets %%%%%%%%%%%%%%%%%%%%

% bioharness summary packet
sd_start_time = [];
hr_data = [];
br_data = [];
hrv_data = [];
sd_time = [];

% bioharness rr packet
rr_start_time = [];
rr_time = [];
rr_data = [];
current_rr = [];

 %%%%%%%%%%%%%%%%%%%%%%%  qsensor data packet %%%%%%%%%%%%%%%%%%%%
qs_start_time = [];
eda_data = [];
eda_time = [];

%%%%%%%%%%%%%%%%%%%%%%%% haptic state variables %%%%%%%%%%%%%%%%%%
truthful_heartrate = 0;
hb_t0 = 0;

truthful_breathrate = 0;
br_t0 = 0;
inhalation_time = 4;
exhalation_time = 4;


%%%%%%%%%%%%%%%%%% variables for bioharness experiment %%%%%%%%%%%%%%%%%%
count = 0;
duration = 1;
percent_bpm = 1;
freq_hr = 80;
volume_hr = 100;
freq_br = 80;
volume_br = 100;
lowlimit_hr = 60;
limit_br = 10;
BH_Data = [];
start_time = cputime;
hr_array_length = 0;
br_array_length = 0;
hr_out_data=[];
br_out_data=[];
avg_hr = 0;
avg_br = 0;
last_const_hr = 0;
last_const_br = 0;
bpm_const_hr = 0;
bpm_const_br = 0;

myAudioRecording2(8000,2,8000);

%%%%%%%%%%%%%%%%%%%%%%%%% ui elements %%%%%%%%%%%%%%%%%%%%%%%

% main figure
hFigure = figure('Visible', 'off', 'Position', [100,100,1250,580], ...
    'Resize', 'off', 'NumberTitle', 'off', 'ToolBar', 'none', ...
    'Name', 'HapLand Biofeedback', 'MenuBar', 'none', ...
    'DeleteFcn', @gui_del_fcn);

bgcolor = get(hFigure,'color');

% positions: from left, from bottom, width, height
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% plots %%%%%%%%%%%%%%%%%%%%%%%%%%%

%heart rate plot
hr_axes = axes('units', 'pixels', 'position', [75,400,340,150]);
hr_plot = plot(0,0, '.-', 0, 0, '-', 0, 0, '-');
grid on;
ylabel('BPM', 'FontSize', 8);
ylim([40 120]);

% hr average text
hHR_avg = uicontrol('style', 'text', ...
    'backgroundcolor', bgcolor,...
    'position', [80,550,170,20],...
    'fontsize', 10,...
    'HorizontalAlignment', 'left', ...
    'string', 'Heart rate avg:');

% br average text
hBR_avg = uicontrol('style', 'text', ...
    'backgroundcolor', bgcolor,...
    'position', [495,550,170,20],...
    'fontsize', 10,...
    'HorizontalAlignment', 'left', ...
    'string', 'Breath rate avg:');

% current hr text
hHR_text = uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
    'position', [290,550,120,20], 'fontsize', 10,...
    'HorizontalAlignment', 'left', 'string', 'Heart rate:');

% breathing rate plot
br_axes = axes('units', 'pixels', 'position', [490,400,340,150]);
br_plot = plot(0,0, '.-', 0, 0, '-', 0, 0, '-');
ylabel('BPM', 'FontSize', 8);
ylim([0 40]);
grid on;

% current br text
hBR_text = uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
    'position', [700,550,150,20], 'fontsize', 10,...
    'HorizontalAlignment', 'left', 'string', 'Breathing rate:');

% hrv plot
hrv_axes = axes('units', 'pixels', 'position', [75,180,340,150]);
hrv_plot = plot(0,0, '.-');
grid on;
ylabel('HRV (ms)', 'FontSize', 8);
ylim([0 250]);

% current hrv text
hHRV_text = uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
    'position', [130,330,290,20], 'fontsize', 10,...
    'HorizontalAlignment', 'left', ...
    'string', 'Rolling 300 heartbeat SDNN HRV (ms):');

hEDA_text = uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
    'position', [1040,550,120,20], 'fontsize', 10,...
    'HorizontalAlignment', 'left', 'string', 'EDA');

% rr plot
mic_axes = axes('units', 'pixels', 'position', [490,180,340,150]);
mic_plot = plot(0,0);
%ylabel('RR interval (ms)', 'FontSize', 8);
%ylim([0 1500]);
grid on;

% current rr text
uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
    'position', [620,330,195,20], 'fontsize', 10,...
    'HorizontalAlignment', 'left', 'string', 'Mic Output');

% accelerometer plot
accel_axes = axes('units', 'pixels', 'NextPlot', 'add', 'box', 'on', ...
    'position', [890,20,340,210], 'xtick', [], 'ytick', []);
accel_plot1 = plot(0,0);
accel_plot2 = plot(0,0);
axis([0 1 0 100])
h = impoly(gca,[0.0,0.0 ; 0.1,0.0; 0.2,99.6 ; 0.3,0.0 ; 0.434, 0.0 ; 0.524,26.5 ; 0.605,0.0 ; 0.9,0.0 ; 1.0,0.0], 'Closed', false)
id = addNewPositionCallback(h,@(p) title(mat2str(p,3)));
fcn = makeConstrainToRectFcn('impoly',get(gca,'XLim'),get(gca,'YLim'));
setPositionConstraintFcn(h,fcn);
% accel text 
 uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
     'position', [1020,250,195,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Signal Beat: Heart Rate');
 
 
brbeat_axes = axes('units', 'pixels', 'NextPlot', 'add', 'box', 'on', ...
    'position', [890,320,340,210], 'xtick', [], 'ytick', []);
brbeat_plot1 = plot(0,0);
brbeat_plot2 = plot(0,0);
axis([0 1 0 100])
b = impoly(gca,[0.0,0.0 ; 0.1,56.7; 0.22,86.8 ; 0.34,100 ; 0.476,84.2 ; 0.60,23.1 ; 0.716,1.72 ; 0.9,0.0 ; 1.0,0.0], 'Closed', false)
id = addNewPositionCallback(b,@(p) title(mat2str(p,3)));
fcn = makeConstrainToRectFcn('impoly',get(gca,'XLim'),get(gca,'YLim'));
setPositionConstraintFcn(b,fcn);
% accel text 
 uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
     'position', [1020,550,195,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Signal Beat: Breathing Rate');

 
%%%%%%%%%%%%%%%%%%%%%%% Controls UI Box Param %%%%%%%%%%%%%%%%%%%%%%%%%%
 hp = uipanel('Title', 'Controls', 'fontsize', 10, ...
         'titleposition', 'lefttop', 'position', [.18, .027, .49, .22]);
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [5,80,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Percent BPM');
 toru = uicontrol('parent', hp, 'style', 'edit','string', '100', ...
         'position', [5, 55, 75, 25], 'fontsize', 10);
 hrbox = uicontrol('style', 'checkbox', 'parent', hp, ...
         'position', [5,25,60,25], 'string', 'hr')
 brbox = uicontrol('style', 'checkbox', 'parent', hp, ...
         'position', [5,2,60,25], 'string', 'br')
 constbox = uicontrol('style', 'checkbox', 'parent', hp, ...
         'position', [40,25,60,25], 'string', 'const')
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [100,80,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Freq HR (Hz)');
 freqbox_hr = uicontrol('parent', hp, 'style', 'edit','string', '80', ...
     'position', [100,55,75,25], 'fontsize',10) 
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [100,30,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Volume HR');
 volbox_hr = uicontrol('parent', hp, 'style', 'edit','string', '100', ...
     'position', [100,5,75,25], 'fontsize',10)
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [180,80,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Freq BR (Hz)');
 freqbox_br = uicontrol('parent', hp, 'style', 'edit','string', '80', ...
     'position', [180,55,75,25], 'fontsize',10) 
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [180,30,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Volume BR');
 volbox_br = uicontrol('parent', hp, 'style', 'edit','string', '100', ...
     'position', [180,5,75,25], 'fontsize',10)
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [270,30,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Lwr Lim HR');
 lowlimitbox_hr = uicontrol('parent', hp, 'style', 'edit','string', '60', ...
     'position', [270,5,75,25], 'fontsize',10) 
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [270,80,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Uppr Lim HR');
 uplimitbox_hr = uicontrol('parent', hp, 'style', 'edit','string', '120', ...
     'position', [270,55,75,25], 'fontsize',10) 
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [350,30,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Lwr Lim BR');
 lowlimitbox_br = uicontrol('parent', hp, 'style', 'edit','string', '10', ...
     'position', [350,5,75,25], 'fontsize',10)
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [350,80,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Uppr Lim BR');
 uplimitbox_br = uicontrol('parent', hp, 'style', 'edit','string', '30', ...
     'position', [350,55,75,25], 'fontsize',10)
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [440,80,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Sample_hr');
 samplesizebox_hr = uicontrol('parent', hp, 'style', 'edit','string', '30', ...
     'position', [440,55,75,25], 'fontsize',10)
 uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
     'position', [440,30,100,20], 'fontsize', 10,...
     'HorizontalAlignment', 'left', 'string', 'Sample_br');
 samplesizebox_br = uicontrol('parent', hp, 'style', 'edit','string', '60', ...
     'position', [440,5,75,25], 'fontsize',10)
%  uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
%      'position', [520,80,100,20], 'fontsize', 10,...
%      'HorizontalAlignment', 'left', 'string', 'Const_hr');
%  constbox_hr = uicontrol('parent', hp, 'style', 'edit','string', '60', ...
%      'position', [520,55,75,25], 'fontsize',10)
%  uicontrol('parent', hp, 'style', 'text', 'backgroundcolor', bgcolor,...
%      'position', [520,30,100,20], 'fontsize', 10,...
%      'HorizontalAlignment', 'left', 'string', 'Const_br');
%  constbox_br = uicontrol('parent', hp, 'style', 'edit','string', '60', ...
%      'position', [520,5,75,25], 'fontsize',10)

%%%%%%%%%%%%%%%%%%%%%%  status texts %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% status line
hStatus = uicontrol('style', 'text', 'backgroundcolor', bgcolor,...
    'position', [10,15,170,20], 'fontsize', 8, ...
    'HorizontalAlignment', 'left', 'string', 'Ready');

 % bh system confidence
 hSYS_conf = uicontrol('style', 'text', ...
     'backgroundcolor', bgcolor, 'position', [60,110,1,20],...
     'fontsize', 10, 'HorizontalAlignment', 'left', ...
     'string', 'BH system confidence:');

 % bh battery level
 hBAT_level = uicontrol('style', 'text', ...
     'backgroundcolor', bgcolor, 'position', [60,80,1,20],...
     'fontsize', 10, 'HorizontalAlignment', 'left', ...
     'string', 'BH battery level:');

 % qs battery level
 hQS_bat_text = uicontrol('style', 'text', ...
     'backgroundcolor', bgcolor, 'position', [60,50,1,20],...
     'fontsize', 10, 'HorizontalAlignment', 'left', ...
     'string', 'QS battery level:');

%%%%%%%%%%%%%%%%%%%%%%%%%%% menu %%%%%%%%%%%%%%%%%%%%%%%%%%

hConnectMenu = uimenu(hFigure, 'Label', 'Connect');
uimenu(hConnectMenu, 'Label', 'Bioharness', 'callback', @connect_bh);
uimenu(hConnectMenu, 'Label', 'Q sensor', 'callback', @connect_qs);
uimenu(hConnectMenu, 'Label', 'Haptics', 'callback', @connect_haptic);
uimenu(hConnectMenu, 'Label', 'Accelerometer', 'callback', @connect_accel);

% Reset plot data 
uimenu('label', 'Reset plots', 'callback', @reset_button);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   end ui elements %%%%%%%%%%%%%%%%%%%%%%%

% Ready to go live
set(hFigure, 'Visible', 'on');
disp('start');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    functions   %%%%%%%%%%%%%%%%%%%%%%%


    function reset_button(~, ~)
        resp = questdlg('Erase all plot data?', 'Confirm', 'OK', ...
            'Cancel', 'Cancel');
        switch resp 
            case 'Cancel'
            return;
        end
        
        % summary data
        hr_data = []; br_data = []; hrv_data =[];
        sd_start_time= []; sd_time = [];
        
        % rr data
        rr_start_time = []; rr_time = []; rr_data = [];
 
		%eda data
        qs_start_time = []; eda_data = []; eda_time = [];
		
        %plots
        set(hr_plot, {'XData'}, {0 ; 0; 0}, {'YData'}, {0 ; 0; 0});
        set(br_plot, {'XData'}, {0 ; 0; 0}, {'YData'}, {0 ; 0; 0});
        set(hrv_plot, 'XData', 0, 'YData', 0);
        set(mic_plot, 'XData', 0, 'YData', 0);
        set(eda_plot, 'XData', 0, 'YData', 0)
%        set(eda_axes, 'xlim', [0 plot_time]);
    end

%%%%%%%%%%%%%%%%%%%%%%%%%% connect functions %%%%%%%%%%%%%%%%%%%%%%%%%%

    function connect_bh(obj, ~)
        if (bh_connected == 0)
            set(hConnectMenu, 'enable', 'on');
            set (hStatus, 'String', 'Connecting...'); drawnow;
            bh_conn = serial(bh_port, 'InputBufferSize', 2048);
%           bh_conn = Bluetooth(bh_remote_name, 1);
%           bh_conn.InputBufferSize=2048;
            set (hStatus, 'String', 'Opening bioharness data stream...');
            drawnow;
            try
                fopen(bh_conn);
            catch e
                fclose(bh_conn);
				delete(bh_conn);
                set (hStatus, 'String', 'Error opening bioharness data stream.');
                set(hConnectMenu, 'enable', 'on');
                return;
            end
            try
                set (hStatus, 'String', 'Configuring bioharness...'); drawnow;
                fwrite(bh_conn, uint8([2 164 4 0 0 0 0 0 3])); % Disable timout so we don't to have send keep alive packet
                fwrite(bh_conn, uint8([2 189 2 1 0 196 3])); % Enable summary data packet
                fwrite(bh_conn, uint8([2 25 1 1 94 3])); % Enable RR data packet
                % set RTC
                now = datetime('now');
                time_packet = [now.Day now.Month ...
                    bitand(uint16(now.Year), 15) bitand(uint16(now.Year), 240) ...
                    now.Hour now.Minute ceil(now.Second)];
                fwrite(bh_conn, uint8([2 7 7 time_packet crc_calc(uint8(time_packet)) 3]));
                % ask what time the bioharness has
                fwrite(bh_conn, uint8([2 8 0 0 3]));
            catch e
                fclose(bh_conn);
			 	delete(bh_conn);
                set (hStatus, 'String', 'Error configuring bioharness.');
                 set(hConnectMenu, 'enable', 'on');
                 return;
            end
            bh_connected = 1;
            start(bh_timer);
            start(sound_timer);
            set(hStatus, 'String', 'Ready');
			set(obj, 'checked', 'on')
            set(hConnectMenu, 'enable', 'on');
        else
            set(hConnectMenu, 'enable', 'off');
            bh_connected = 0;
            stop(bh_timer);
            fclose(bh_conn);
            delete(bh_conn);
            set(hHR_text, 'String', 'Heart rate:');
            set(hBR_text, 'String', 'Breathing rate:');
            set(hHR_avg, 'String', 'Heart rate avg:');
            set(hBR_avg, 'String', 'Breath rate avg:');
            set(hSYS_conf, 'String', 'BH system confidence:');
            set(hHRV_text, 'String', 'Rolling 300 heartbeat SDNN HRV (ms):');
            set(hBAT_level, 'String', 'BH battry level:');
            set(hStatus, 'String', 'Ready');
			set(obj, 'checked', 'off')
            set(hConnectMenu, 'enable', 'on');
        end
    end

	function connect_qs(obj, ~)
        if (qs_connected == 0)
            set(hConnectMenu, 'enable', 'on');
            set (hStatus, 'String', 'Connecting Qsensor...'); drawnow;
            qs_conn = serial(qs_port, 'InputBufferSize', 2048);
            set (hStatus, 'String', 'Opening QSensor port...'); drawnow;
            try
                fopen(qs_conn);
            catch e
                fclose(qs_conn);
				delete(qs_conn);
                set (hStatus, 'String', 'Error opening Qsensor data stream.');
                set(hConnectMenu, 'enable', 'on');
                return;
            end
            qs_connected = 1;
            start(qs_timer);
            set(hConnectMenu, 'enable', 'on');
			set(obj, 'checked', 'on')
            set (hStatus, 'String', 'Running'); drawnow;
        else
            set(hConnectMenu, 'enable', 'off');
            qs_connected = 0;
            stop(qs_timer);
            fclose(qs_conn);
			delete(qs_conn);
            set(hEDA_text, 'String', 'EDA:');
            set(hStatus, 'String', 'Ready');
  			set(obj, 'checked', 'off')
            set(hConnectMenu, 'enable', 'on');
        end
     end
	
    function connect_haptic(obj, ~)
        if(haptic_connected == 0)
			set(hConnectMenu, 'enable', 'off');
            set(hStatus, 'String', 'Connecting haptics ...');
            drawnow; 
			haptic_conn = serial(haptic_port);
            set (hStatus, 'String', 'Opening haptic data stream...');
            drawnow;
            try
                fopen(haptic_conn);
            catch e
                fclose(haptic_conn);
				delete(haptic_conn);
                set (hStatus, 'String', 'Error opening haptic data stream.');
                set(hConnectMenu, 'enable', 'on');
                return;
            end
			set(hConnectMenu, 'enable', 'on');
            set(findall(hp, '-property', 'enable'), 'enable', 'on');
            set(hStatus, 'String', 'Ready');
			set(obj, 'checked', 'on')
            drawnow;
            haptic_connected = 1;
        else % disconnect
			set(hConnectMenu, 'enable', 'off');
            set(findall(hp, '-property', 'enable'), 'enable', 'off');
            truthful_heartrate = 0;
            stop(heartbeat_timer);
            stop(breath_timer);
            stop(sequential_timer);
            fclose(haptic_conn);
			delete(haptic_conn);
            haptic_connected = 0;
			set(obj, 'checked', 'off')
			set(hConnectMenu, 'enable', 'on');
        end
    end

    function connect_accel(obj, ~)
        if(accel_connected == 0)
            set(hConnectMenu, 'enable', 'off');
            set(hStatus, 'String', 'Connecting accelerometers ...');
            drawnow; 
			accel_conn = serial(accel_port, 'baudrate', 115200, ...
                'InputBufferSize', 2048);
            set (hStatus, 'String', 'Opening accelerometers data steam...');
            drawnow;
            try
                fopen(accel_conn);
            catch e
                fclose(accel_conn);
				delete(accel_conn);
                set (hStatus, 'String', 'Error opening accelerometer data stream.');
                set(hConnectMenu, 'enable', 'on');
                return;
            end
            start(accel_timer);
            set(hConnectMenu, 'enable', 'on');
            set(hStatus, 'String', 'Ready');
			set(obj, 'checked', 'on')
            drawnow;
            accel_connected = 1;
        else % disconnect
			set(hConnectMenu, 'enable', 'off');
            stop(accel_timer);
            fclose(accel_conn);
			delete(accel_conn);
            accel_connected = 0;
			set(obj, 'checked', 'off')
			set(hConnectMenu, 'enable', 'on');
        end
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%% haptic control functions %%%%%%%%%%%%%%%%%%%%%%%%%
	
	function truthful_heartbeat(obj, ~)
		if obj.Value == 1  % checked
			hHREdit.String = '';
			hHRUpperThreshold.String = '';
			hHRLowerThreshold.String = '';
            stop(heartbeat_timer);
			play_heartbeat;
			truthful_heartrate = 1;
			hb_t0 = clock();
        else % unchecked
			truthful_heartrate = 0;
		end		
	end
	
    function user_heartrate(obj, ~)
        rate = str2double(get(obj, 'String'));
		if isnan(rate) || rate < 1
			stop(heartbeat_timer);
			obj.String = '';
			return;
		end
		hTrueHeartrateBox.Value = 0;
        truthful_heartrate = 0;
		hHRUpperThreshold.String = '';
		hHRLowerThreshold.String = '';
        stop(heartbeat_timer);
		set(heartbeat_timer, 'Period', 60/rate);
		start(heartbeat_timer);
    end

    function user_eda(obj, ~)
        if isnan(str2double(obj.String))
            obj.String = '';
        else
            hTrueHeartrateBox.Value = 0;
            hHREdit.String = '';
        end
    end

    function play_heartbeat(~, ~)
		fwrite(haptic_conn, ...
			['R', 9, 220, 220, bitsplit(100), bitsplit(150), ...
			bitsplit(100), bitsplit(0), 1]);
    end

    function truthful_breath(obj, ~)
		if obj.Value == 1  % checked
			hBRInhalationEdit.String = '';
			hBRExhalationEdit.String = '';
            stop(breath_timer);
			truthful_breathrate = 1;
			br_t0 = clock();
            inhalation_time = 3;
            exhalation_time = 3;
            play_breath;
		else
			truthful_breathrate = 0;
		end		
    end

    function play_breath(~, ~)
        fwrite(haptic_conn, ['M', 10, 175, 200, bitsplit(inhalation_time*1000), 2, 1]);
        fwrite(haptic_conn, ['M', 10, 200, 175, bitsplit(exhalation_time*1000), 2, 1]);
    end

    function changeInhalation(obj, ~)
        stop(breath_timer);
		len = str2double(get(obj, 'String'));
		if ~isempty(len)
            inhalation_time = len;
			set(breath_timer, 'Period', inhalation_time + exhalation_time);
            start(breath_timer);
        else
			set(obj, 'String', '');
		end
    end

    function changeExhalation(obj, ~)
        stop(breath_timer);
		len = str2double(get(obj, 'String'));
		if ~isempty(len)
            exhalation_time = len;
			set(breath_timer, 'Period', inhalation_time + exhalation_time);
            start(breath_timer);
        else
			set(obj, 'String', '');
		end
    end


%%%%%%%%%%%%%%%%%%%%%%%%%%% data processing funcitons %%%%%%%%%%%%%%%%

    function read_accel_data(~, ~)
        if accel_conn.bytesavailable < 50
            return
        end
        persistent data plot1_data plot2_data;
        if isempty(data); data=[]; plot1_data=[]; plot2_data=[]; end
        data = [data int16(fread(accel_conn, accel_conn.bytesavailable))'];
        % find indexes
        idxs = find(data(1:end-8) == 10);
        for i = 1:length(idxs)-1 % iterate over indexes
            if  data(idxs(i)+8) ~= 10
                continue;
            end
            x = bitor(bitshift(data(idxs(i)+2),8), data(idxs(i)+3), 'int16');
            y = bitor(bitshift(data(idxs(i)+4),8), data(idxs(i)+5), 'int16');
            z = bitor(bitshift(data(idxs(i)+6),8), data(idxs(i)+7), 'int16');
            x = double(x) / 5;
            y = double(y) / 5;
            z = double(z) / 5;
            mag = sqrt(x^2 + y^2 + z^2);
			if data(idxs(i)+1) == '1'   % '1'
				plot1_data = [plot1_data, mag];
			elseif data(idxs(i)+1) == '2'  % '2'
				plot2_data = [plot2_data, mag+2500];
			end          
        end
        % remove data
        data = data(idxs(i):end);
        if length(plot1_data) > 2000
            plot1_data = plot1_data(100:end);
        end
        if length(plot2_data) > 2000
            plot2_data = plot2_data(100:end);
        end
        set(accel_plot1, 'ydata', plot1_data, 'xdata', 1:length(plot1_data));
        set(accel_plot2, 'ydata', plot2_data, 'xdata', 1:length(plot2_data));
        drawnow;
    end

    function read_qs_data(~, ~)
        if qs_conn.bytesavailable == 0
            return
		end
        d = fread(qs_conn, qs_conn.bytesavailable);
        persistent partial qs_bat;
        c = [partial char(d)'];
        l = strsplit(c, '\n'); %split character vector into lines
		ts = now; % timestamp, when we received this data 
		if( isempty(qs_start_time))
			qs_start_time = ts;
		end
        for i=1:length(l)
            z = strsplit(l{i}, ','); % split lines on comma
            if length(z) == 7  % if this is a complete line
                qs_bat = str2double(z{5});
                eda_data= [eda_data  str2double(z{7})]; %eda reading
                eda_time = [eda_time (ts - qs_start_time)*24*60*60 + (i-1)/16];
            else
                partial = l{i}; % save incomplete line for next pass
            end
        end
        if length(eda_data) > plot_time * 16  
            eda_data = eda_data(5*16+1:end);
            eda_time = eda_time(5*16+1:end);
            set(eda_axes, 'XLim', [eda_time(1) eda_time(end)+5]);
        end
        set(eda_plot, 'XData', eda_time, 'YData', eda_data);
        format short;
        set(hQS_bat_text, 'String', sprintf('QS battery level: %.2f', qs_bat));
        drawnow;
        %  play heartbeat if threshold exceeded
		upper = str2double(hHRUpperThreshold.String);
        if (~isnan(upper)) &&  (eda_data(end) > upper) ...
                && (length(heartbeat_timer.running) == 3) 
                    heartbeat_timer.period = 60/50; % 50 bpm
                    start(heartbeat_timer);
                    disp('hi there')
                    %start(sound_timer);
        end
		lower = str2double(hHRLowerThreshold.String);
        if ~isnan(lower) &&  eda_data(end) < lower && length(heartbeat_timer.running) == 3 
                    heartbeat_timer.period = 60/80; 
                    start(heartbeat_timer);
                    disp('nawwww bra')
                    %start(sound_timer);
        end
        if ~isnan(lower) &&  ~isnan(upper) && eda_data(end) > lower && eda_data(end) < upper 
                    stop(heartbeat_timer);
                    disp('offffff')
                    %stop(sound_timer);
        end
    end

    function read_bh_packets(~, ~)
        if (bh_conn.bytesAvailable == 0)
            return;
        end
        ps = [ps fread(bh_conn, bh_conn.bytesAvailable)'];
        idxs = find(ps == 2); % 0x02 marks start of a msg
        %fprintf('length ps: %d\n', length(ps));
        % process all potential msg start indexes in data stream
        while (~isempty(idxs) && (length(ps) > 5))
            if (ps(idxs(1)+1) == 43 && ps(idxs(1)+2) == 71 && ...
                    length(ps(idxs(1):end)) > 75)
                % stx + id + dlc + 71 + crc + etx = 76,
                % we have a complete summary data packet
                % dlc = ps(idxs(1)+2);  % should always be 71
                %fprintf('Received crc: %d\n', data(idxs(i)+3+len));
                %fprintf('Calculated crc: %d\n', crc_calc(new_data));
                new_data = ps(idxs(1):idxs(1)+75);
                process_sd(new_data);
                ps = ps(idxs(1)+76:end); % remove this packet
                idxs = find(ps ==2); % update idxs, skip 0x02 inside packet
                continue;
            end
            if (ps(idxs(1)+1) == 36 && ps(idxs(1)+2) == 45 && ...
                    length(ps(idxs(1):end)) > 49)
                % stx + id + dlc + 45 + crc + etx = 50,
                % we have a complete RR data packet
                new_data = ps(idxs(1):idxs(1)+49);
                process_rr(new_data);
                ps = ps(idxs(1) + 50:end); % remove this packet
                idxs = find(ps ==2); % update idxs, skip 0x02 inside packet
                continue;
            end
            if (ps(idxs(1)+1) == 8 && ps(idxs(1)+2) == 7 && ...
                    length(ps(idxs(1):end)) > 7)
                % we have a get RTC Date/Time message
                fprintf('BH time: %2d:%2d:%2d\n', ps(idxs(1)+7), ps(idxs(1)+8), ...
                    ps(idxs(1)+9) );
                ps = ps(idxs(1) + 11:end); % remove this packet
                idxs = find(ps ==2); % update idxs, skip 0x02 inside packet
                continue;
            end
            
            len = ps(idxs(1)+2);
            fprintf('Other or incomplete packet of type 0x%x, length %d\n', ...
                ps(idxs(1)+1), len );
            if length(ps(idxs(1):end)) < len + 5 % incomplete packet
                return;
            end
            %        start      payload   id-dlc-crc-etx
            ps = ps(idxs(1) + ps(idxs(1)+2) + 5:end); % remove this packet
            idxs = find(ps == 2); % update idxs
        end
    end

    function process_sd(data)
% heart rate
        hr_data = [hr_data data(14)];
        if(~isempty(BH_Data))
            hr_out_data = [hr_out_data BH_Data(end,3)];
        else
            hr_out_data = [hr_out_data -1];
        end
        if (truthful_heartrate == 1) && (etime(clock(), hb_t0) >= 60/data(14))
            hb_t0 = clock();
            play_heartbeat;
        end
        set(hHR_text, 'String', sprintf('Heart rate: %d', data(14)));
% breathing rate
        br = bitor(data(16), bitshift(data(17), 8));
        br = br/10;
        if(~isempty(BH_Data))
            br_out_data = [br_out_data BH_Data(end,4)];
        else
            br_out_data = [br_out_data -1];
        end
        if (truthful_breathrate == 1) && (etime(clock(), br_t0) >= br)
            inhalation_time = br/2;
            exhalation_time = br/2;
            br_t0 = clock();
            play_breath;
        end
        set(hBR_text, 'String', ...
            sprintf('Breathing rate: %.1f', br));
        br_data = [br_data br];
% heart rate variability
        hrv = bitor(data(38), bitshift(data(39), 8));
        hrv_data = [hrv_data hrv/100];
        set(hHRV_text, 'String', ...
            sprintf('Rolling 300 heartbeat SDNN HRV (ms): %.2f', hrv/100));
% time stamp
        ts = bitor(data(9), bitshift(data(10), 8));
        ts = bitor(ts, bitshift(data(11), 16));
        ts = bitor(ts, bitshift(data(12), 24));
        ts = ts / 1000; % convert ms to seconds
        if (isempty(sd_start_time))
            sd_start_time = ts;
        end
        ts = ts - sd_start_time;
        sd_time = [sd_time ts];
% update plots
        samplesize_hr = str2double(samplesizebox_hr.String);
        samplesize_br = str2double(samplesizebox_br.String);
        if(length(hr_data)>=30)
            avg_hr = mean(hr_data(end-samplesize_hr+1:end))*ones(1,length(hr_data));
        else
            avg_hr = mean(hr_data(1:end))*ones(1,length(hr_data));
        end
        if(length(br_data)>=60)
            avg_br = mean(br_data(end-samplesize_br+1:end))*ones(1,length(br_data));
        else
            avg_br = mean(br_data(1:end))*ones(1,length(br_data));
        end
        if length(sd_time) > plot_time * 1  
            hr_data = hr_data(6:end);
            avg_hr = mean(hr_data(end-samplesize_hr+1:end))*ones(1,length(hr_data));
            hrv_data = hrv_data(6:end);
            br_data = br_data(6:end);
            avg_br = mean(br_data(end-samplesize_hr+1:end))*ones(1,length(br_data));
            sd_time = sd_time(6:end);
            set(hr_axes, 'XLim', [sd_time(1) sd_time(end)+5]);
            set(hrv_axes, 'XLim', [sd_time(1) sd_time(end)+5]);
            set(br_axes, 'XLim', [sd_time(1) sd_time(end)+5]);
        end
        if(~isempty(BH_Data))
            if(hr_out_data(end) == -1 && br_out_data(end) == -1)
                set(hr_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {hr_data ; avg_hr; zeros(1,length(sd_time))});
            elseif(hr_out_data(end) > -1 && br_out_data(end) == -1)
                set(hr_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {hr_data ; avg_hr; hr_out_data(end-length(sd_time)+1:end)});
            elseif(hr_out_data(end) == -1 && br_out_data(end) > -1)
                set(hr_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {hr_data ; avg_hr; zeros(1,length(sd_time))});
            else
                set(hr_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {hr_data ; avg_hr; zeros(1,length(sd_time))});
            end
            
            if(hr_out_data(end) == -1 && br_out_data(end) == -1)
                set(br_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {br_data ; avg_br; zeros(1,length(sd_time))});
            elseif(hr_out_data(end) == -1 && br_out_data(end) > -1)
                set(br_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {br_data ; avg_br; br_out_data(end-length(sd_time)+1:end)});
            elseif(hr_out_data(end) > -1 && br_out_data(end) == -1)
                set(br_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {br_data ; avg_br; zeros(1,length(sd_time))});
            else
                set(br_plot, {'XData'}, {sd_time ; sd_time; sd_time}, {'YData'}, {br_data ; avg_br; zeros(1,length(sd_time))});
            end
        end
        disp(avg_hr(1));
        %set(hr_plot, 'XData', sd_time, 'YData', avg_hr);
        %set(br_plot, 'XData', sd_time, 'YData', br_data);
        set(hrv_plot, 'XData', sd_time, 'YData', hrv_data);
% heart rate average
        set(hHR_avg, 'String', ...
            sprintf('Heart rate avg: %d \n', round(avg_hr)));
% breathing rate average
        set(hBR_avg, 'String', ...
            sprintf('Breath rate avg: %d \n', round(avg_br)));
% system confidence
        set(hSYS_conf, 'String', ...
            sprintf('BH system confidence: %d%%', data(41)));
% battery level
        set(hBAT_level, 'String', ...
            sprintf('BH battery level: %d%%', data(28)));
    end

    function process_rr(data)
% time stamp
        ts = bitor(data(9), bitshift(data(10), 8));
        ts = bitor(ts, bitshift(data(11), 16));
        ts = bitor(ts, bitshift(data(12), 24));
        if (isempty(rr_start_time))
            rr_start_time = ts;
        end
        ts = ts - rr_start_time;
% rr data
        for i=0:17  % 18 bytes
            rr = bitor(data(i*2+13), bitshift(data(i*2+14), 8));
            if (rr > 32767); rr = -(65536 - rr); end
            rr_data = [rr_data rr];
            rr_time = [rr_time ts/1000 + 0.056*i];
        end
        
        % update current rr
        current_rr = rr_data(end-17:end);
        
        if length(rr_data) > 18 * plot_time 
            rr_data = rr_data(5*18+1:end);
            rr_time = rr_time(5*18+1:end);
           set(mic_axes, 'XLim', [rr_time(1) rr_time(end)+5]);
        end

        set(mic_plot, 'XData', rr_time, 'YData', rr_data);  
    end


    function gui_del_fcn(~, ~)
        delete(timerfindall);
        delete(instrfindall);
        disp('exit');
        disp(BH_Data);
        dlmwrite('BioHarnessData.csv', BH_Data,'delimiter',',');
    end

    function Bioharness_OUTPUT(~,~)
        tempdata=[];
        if(hrbox.Value==1) %if box to activate heart rate is checked
            if(isempty(hr_data)==0) %if array storing heart rate is not empty
                count= count+1;
                if(count*0.01> duration) %check is current beat is being played
                    bpm = hr_data(end) %get most recent heartbeat
                    if(bpm~=0)
                        tempdata = [hr_data(end) br_data(end)];
                        %%%%%%%%%%get data from the GUI input boxes%%%%%%%
                        percent_bpm = str2double(toru.String)/100;
                        freq_hr = str2double(freqbox_hr.String);
                        volume_hr = str2double(volbox_hr.String)/100;
                        lowlimit_hr = str2double(lowlimitbox_hr.String);
                        uplimit_hr = str2double(uplimitbox_hr.String);
                        
                        %check if limit is being exceeded
                        if(constbox.Value ~= 1) %if const box is not checked, run normally
                            last_const_hr = 0;
                            if(percent_bpm*bpm > lowlimit_hr && percent_bpm*bpm < uplimit_hr)
                                bpm = percent_bpm*bpm;
                                duration = Sound_Warble(bpm, getPosition(h), freq_hr, volume_hr);
                                disp(bpm)
                                tempdata = [tempdata bpm -1 cputime-start_time];
                            elseif(percent_bpm*bpm <= lowlimit_hr)
                                duration = Sound_Warble(lowlimit_hr, getPosition(h), freq_hr, volume_hr);
                                disp('we have hit the limit')
                                disp(lowlimit_hr)
                                tempdata = [tempdata lowlimit_hr -1 cputime-start_time];
                            elseif(percent_bpm*bpm >= uplimit_hr)
                                duration = Sound_Warble(uplimit_hr, getPosition(h), freq_hr, volume_hr);
                                disp('we have hit the limit')
                                disp(uplimit_hr)
                                tempdata = [tempdata uplimit_hr -1 cputime-start_time];
                            end
                        else % if const box is checked get last bpm and use that as the const
                            if(last_const_hr == 0)
                                bpm_const_hr = bpm;
                            end
                            last_const_hr = 1;
                            const_bpm = percent_bpm*bpm_const_hr;
                            duration = Sound_Warble(const_bpm, getPosition(h), freq_hr, volume_hr);
                            tempdata = [tempdata const_bpm -1 cputime-start_time];
                        end
                    end
                    count = 0;
                end
            end
        elseif(brbox.Value==1) %if box to activate breathing rate is checked
            if(isempty(br_data)==0) %if array storing breathing rate is not empty
                count= count+1;
                if(count*0.01> duration) %check is current beat is being played
                    bpm = br_data(end) %get most recent heartbeat
                    if(bpm~=0)
                        tempdata = [hr_data(end) br_data(end)];
                        %%%%%%%%%%get data from the GUI input boxes%%%%%%%
                        percent_bpm = str2double(toru.String)/100;
                        freq_br = str2double(freqbox_br.String);
                        volume_br = str2double(volbox_br.String)/100;
                        lowlimit_br = str2double(lowlimitbox_br.String);
                        uplimit_br = str2double(uplimitbox_br.String);
                        
                        %check if limit is being exceeded
                        if(constbox.Value ~= 1) %if const box is not checked, run normally
                            last_const_br = 0;
                            if(percent_bpm*bpm > lowlimit_br && percent_bpm*bpm < uplimit_br)
                                bpm = percent_bpm*bpm;
                                duration = Sound_Warble(bpm, getPosition(b), freq_br, volume_br);
                                disp(bpm)
                                tempdata = [tempdata -1 bpm cputime-start_time];
                            elseif(percent_bpm*bpm <= lowlimit_br)
                                duration = Sound_Warble(lowlimit_br, getPosition(b), freq_br, volume_br);
                                disp('we have hit the limit')
                                disp(lowlimit_br)
                                tempdata = [tempdata -1 lowlimit_br cputime-start_time];
                            elseif(percent_bpm*bpm >= uplimit_br)
                                duration = Sound_Warble(uplimit_br, getPosition(b), freq_br, volume_br);
                                disp('we have hit the limit')
                                disp(uplimit_br)
                                tempdata = [tempdata -1 uplimit_br cputime-start_time];
                            end
                        else % if const box is checked get last bpm and use that as the const
                            if(last_const_br == 0)
                                bpm_const_br = bpm;
                            end
                            last_const_br = 1;
                            const_bpm = percent_bpm*bpm_const_br;
                            duration = Sound_Warble(const_bpm, getPosition(b), freq_br, volume_br);
                            tempdata = [tempdata -1 const_bpm cputime-start_time];
                        end
                    end
                    count = 0;
                end
            end
        else %if no boxes are checked, input -1 as the outputs for both br and hr
            if(numel(hr_data)>hr_array_length || numel(br_data)>br_array_length)
                tempdata = [hr_data(end) br_data(end) -1 -1 cputime-start_time];
                hr_array_length = numel(hr_data);
                br_array_length = numel(br_data);
            end
        %store data on arr
        end
        disp(tempdata)
        if(isempty(tempdata) == 0)
             BH_Data = [BH_Data; tempdata];
             tempdata = [];    
         end
    end
end
