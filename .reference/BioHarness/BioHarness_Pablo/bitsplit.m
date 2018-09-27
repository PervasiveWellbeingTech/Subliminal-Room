function [x] = bitsplit (input)
    x(1) = bitshift(input, -8);
    x(2) = bitand(255, input);
end


