% Program to create a warbling wave file with variable amplitude and pitch.
%
function duration = Sound_Warble(bpm,coords, freq, volume)
t = 60/(bpm); %period of each beat in seconds
fs=8192;  % sampling frequency
beats = 1; %sound runs for 1 beats until it samples again (this can be changed)
num_samples = floor(fs*t); %number of samples in each beat

beat_shape = [linspace(coords(1,2),coords(2,2),floor((coords(2,1)-coords(1,1))*num_samples))... %gets the beat shape from the interactive graph
    linspace(coords(2,2),coords(3,2), floor((coords(3,1)-coords(2,1))*num_samples)) ...
    linspace(coords(3,2),coords(4,2), floor((coords(4,1)-coords(3,1))*num_samples)) ...
    linspace(coords(4,2),coords(5,2), floor((coords(5,1)-coords(4,1))*num_samples)) ... 
    linspace(coords(5,2),coords(6,2), floor((coords(6,1)-coords(5,1))*num_samples)) ...
    linspace(coords(6,2),coords(7,2), floor((coords(7,1)-coords(6,1))*num_samples)) ...
    linspace(coords(7,2),coords(8,2), floor((coords(8,1)-coords(7,1))*num_samples)) ...
    linspace(coords(8,2),coords(9,2), floor((coords(9,1)-coords(8,1))*num_samples)) ...
    ]./100;
duration=beats*t;
amp = repmat(beat_shape, 1,beats);%how many beats will be played before the program samples again
values=linspace(0, t, fs*t);

%creating extra zeros at the end of the signal to make sure the...
% 'values' array and the amp array match size
if(size(values,2) > size(amp,2)) 
    num_zeros = size(values,2)-size(amp,2);
    amp = [amp zeros(1,num_zeros)];
end
if(size(values,2)< size(amp,2))
    num_zeros = -(size(values,2)-size(amp,2));
    values = [values zeros(1,num_zeros)];
end

a=volume*amp.*sin(2*pi* freq*values);
% figure(121)
% plot(values, a)
 
sound(a, fs)

end