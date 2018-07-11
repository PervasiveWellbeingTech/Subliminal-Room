function crc = crc_calc (block)
        crc = 0;
        for i = 1:length(block)
                crc = bitxor(crc, block(i), 'uint8');
                for k = 1:8
                   if (bitand(crc, 1, 'uint8') ~= 0)
                       crc = bitxor( bitshift(crc, -1, 'uint8'), 140, 'uint8');
                   else
                       crc = bitshift(crc, -1, 'uint8');
                   end
                end
        end

end
