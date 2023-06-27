function m20225571_p2()
    clc; clear; close all;
    function plot_filters(upsample_factor)
        
        % Define the interpolation factors
        L = upsample_factor; 
        
        % Generate the sample-and-hold filter
        h_sah = ones(1, L);
        
        % Generate the linear interpolation filter
        h_lin = zeros(1, 2*L+1);
        for n = -L:L
            h_lin(n+L+1) = sinc(n/2);
        end
        
        % Generate the cubic convolution filter
        a = -0.5;
        h_cc = zeros(1, 4*L+1);
        for n = -2*L:2*L
            h_cc(n+2*L+1) = (a+2)*abs(n)^3 - (a+3)*abs(n)^2 + 1;
            h_cc(n+2*L+1) = h_cc(n+2*L+1) * sinc(n/2*(1-a));
        end
            
        % Plot the impulse and frequency responses of the filters
        figure;
        impz(h_sah);
        title('Sample-and-Hold Impulse Response');
        figure;
        freqz(h_sah);
        title('Sample-and-Hold Frequency Response');
        
        figure;
        impz(h_lin);
        title('Linear Interpolation Impulse Response');
        figure;
        freqz(h_lin);
        title('Linear Interpolation Frequency Response');
        
        figure;
        impz(h_cc);
        title('Cubic Convolution Interpolation Impulse Response');
        figure;
        freqz(h_cc);
        title('Cubic Convolution Interpolation Frequency Response');
    end
    
    function run_scaler()
        I = im2double(imread("barbara.png"));
        
        L = 3; 
        M = 2;

        I_sah_up = imresize(I, L, "nearest");
        I_lin_up =  imresize(I, L, 'bilinear');
        I_cub_up = imresize(I, L, 'cubic');
        % Generate the sample-and-hold filter
        
        third_h_lin =  fir1(2, 1/3, 'low');
        third_h_cc = fir1(2, 1/3, 'low');
        third_h_sah = fir1(2, 1/3, 'low');
        half_h_lin = fir1(2, 0.5, 'low');
        half_h_sah = fir1(2, 0.5, 'low');
        half_h_cc = fir1(2, 0.5, 'low');

        third_h_sah = third_h_sah'*third_h_sah;
        third_h_lin = third_h_lin'*third_h_lin;
        third_h_cc = third_h_cc'*third_h_cc;

        half_h_sah = half_h_sah'*half_h_sah;
        half_h_lin = half_h_lin'*half_h_lin;
        half_h_cc = half_h_cc'*half_h_cc;
        
        if L == 3
            I_sah = imfilter(I_sah_up, third_h_sah);
            I_lin = imfilter(I_lin_up, third_h_lin);
            I_cub = imfilter(I_cub_up, third_h_cc);
        else
            I_sah = imfilter(I_sah_up, half_h_sah);
            I_lin = imfilter(I_lin_up, half_h_lin);
            I_cub = imfilter(I_cub_up, half_h_cc);
        end

        if M == 3
            I_sah_aa = imfilter(I_sah, third_h_sah);
            I_lin_aa = imfilter(I_lin, third_h_lin);
            I_cub_aa = imfilter(I_cub, third_h_cc);
        else
            I_sah_aa = imfilter(I_sah, half_h_sah);
            I_lin_aa = imfilter(I_lin, half_h_lin);
            I_cub_aa = imfilter(I_cub, half_h_cc);
        end
        figure; imshow(I_cub_aa); title("Before downsample"); 
        I_sah_out = downsample(downsample(I_sah_aa', M)', M);
        I_lin_out =  downsample(downsample(I_lin_aa', M)', M);
        I_cub_out = downsample(downsample(I_cub_aa', M)', M);
        
        figure; imshow(I_sah_out); title('Sample-and-Hold Interpolation');
        figure; imshow(I_lin_out); title('Linear Interpolation');
        figure; imshow(I_cub_out); title('Cubic Convolution Interpolation');

        L = 2; 
        M = 3;
        
        I_sah_up = imresize(I_sah_out, L, "nearest");
        I_lin_up =  imresize(I_lin_out, L, 'bilinear');
        I_cub_up = imresize(I_cub_out, L, 'cubic');

        if L == 3
            I_sah = imfilter(I_sah_up, third_h_sah);
            I_lin = imfilter(I_lin_up, third_h_lin);
            I_cub = imfilter(I_cub_up, third_h_cc);
        else
            I_sah = imfilter(I_sah_up, half_h_sah);
            I_lin = imfilter(I_lin_up, half_h_lin);
            I_cub = imfilter(I_cub_up, half_h_cc);
        end

        
        if M == 3
            I_sah_aa = imfilter(I_sah, third_h_sah);
            I_lin_aa = imfilter(I_lin, third_h_lin);
            I_cub_aa = imfilter(I_cub, third_h_cc);
        else
            I_sah_aa = imfilter(I_sah, half_h_sah);
            I_lin_aa = imfilter(I_lin, half_h_lin);
            I_cub_aa = imfilter(I_cub, half_h_cc);
        end
        I_sah_out = downsample(downsample(I_sah_aa', M)', M);
        I_lin_out =  downsample(downsample(I_lin_aa', M)', M);
        I_cub_out = downsample(downsample(I_cub_aa', M)', M);

        figure; imshow(I_sah_out); title('Sample-and-Hold Interpolation');
        figure; imshow(I_lin_out); title('Linear Interpolation');
        figure; imshow(I_cub_out); title('Cubic Convolution Interpolation');

        sah_mse = immse(im2double(imread("barbara.png")), I_sah_out);
        lin_mse = immse(im2double(imread("barbara.png")), I_lin_out);
        cub_mse = immse(im2double(imread("barbara.png")), I_cub_out);
        fprintf("SAH mse difference %f\n", sah_mse);
        fprintf("LIN mse difference %f\n", lin_mse);
        fprintf("CUB mse difference %f\n", cub_mse);
        figure; imshow(abs(I_sah_out-im2double(imread("barbara.png")))); title("Absolute Errors (Sample-and-Hold)");
        figure; imshow(abs(I_lin_out-im2double(imread("barbara.png")))); title("Absolute Errors (Linear)");
        figure; imshow(abs(I_cub_out-im2double(imread("barbara.png")))); title("Absolute Errors (Cubic)");
    end
    
    function run_demosaic()
        original = imread("kodim07.png");
        red_channel = im2double(imread("kodim07r.png"));
        green_channel = im2double(imread("kodim07g.png"));
        blue_channel = im2double(imread("kodim07b.png"));
        mosaic_image = cat(3, red_channel, green_channel, blue_channel);
        rbcubicFilter = [1/2 1 1/2];
        %rbcubicFilter = rbcubicFilter'*rbcubicFilter;
        gcubicFilter = 1/4.*[0 1 0; 1 4 1; 0 1 0];
        % Demosaic the R channel
        R = red_channel;
        R_horizontal = imfilter(R, rbcubicFilter);
        R_vertical = imfilter(R_horizontal', rbcubicFilter)';

        % Demosaic the B channel
        B = blue_channel;
        B_horizontal = imfilter(B, rbcubicFilter);
        B_vertical = imfilter(B_horizontal', rbcubicFilter)';

        % Demosaic the G channel
        G = green_channel;
        G_H = imfilter(G,  gcubicFilter);
        G_V = imfilter(G', gcubicFilter)';
        G_HV = (G_H + G_V)/2;

        reconstructed_image_1 = cat(3,R_vertical,G_HV,B_vertical);
        figure; imshow(reconstructed_image_1); title("Cubic interpolation");

        mosaic_image = cat(3, red_channel, green_channel, blue_channel);
        g_rb_filter = [0 0 -1 0 0;
                       0 0 2 0 0;
                       -1 2 4 2 -1;
                       0 0 2 0 0;
                       0 0 -1 0 0] / 8;
       rb_g_0_filter = [ 0 0 1/2 0 0;
                         0 -1 0 -1 0;
                         -1 4 5 4 -1;
                         0 -1 0 -1 0;
                         0 0 1/2 0 0] / 8;
       rb_g_1_filter = rb_g_0_filter';
       rb_br_filter = [ 0 0 -3/2 0 0;
                        0 2 0 2 0;
                        -3/2 0 6 0 -3/2;
                        0 2 0 2 0;
                        0 0 -3/2 0 0] / 8;
       % padded_cfa = paddarray_symmetric(cfa_image, 2);
       mosaic_g_rb_filter = imfilter(mosaic_image, g_rb_filter);
       mosaic_rb_g_0_filter = imfilter(mosaic_image, rb_g_0_filter);
       mosaic_rb_g_1_filter = imfilter(mosaic_image, rb_g_1_filter);
       mosaic_rb_br_filter = imfilter(mosaic_image, rb_br_filter);
       
       % 2. Get the rgb image.
       reconstructed_image_2 = zeros(size(mosaic_image,1),size(mosaic_image,2),3);
       % g channel
       reconstructed_image_2(:,:,2) = green_channel;
       reconstructed_image_2(1:2:end,1:2:end,2) = mosaic_g_rb_filter(1:2:end,1:2:end, 2);
       reconstructed_image_2(2:2:end,2:2:end,2) = mosaic_g_rb_filter(2:2:end,2:2:end, 2);
       % r channel
       reconstructed_image_2(:,:,1) = red_channel;
       reconstructed_image_2(1:2:end,2:2:end,1) = mosaic_rb_g_0_filter(1:2:end,2:2:end, 1);
       reconstructed_image_2(2:2:end,1:2:end,1) = mosaic_rb_g_1_filter(2:2:end,1:2:end, 1);
       reconstructed_image_2(2:2:end,2:2:end,1) = mosaic_rb_br_filter(2:2:end,2:2:end, 1);
       % b channel
       reconstructed_image_2(:,:,3) = blue_channel;
       reconstructed_image_2(1:2:end,2:2:end,3) = mosaic_rb_g_1_filter(1:2:end,2:2:end, 3);
       reconstructed_image_2(2:2:end,1:2:end,3) = mosaic_rb_g_0_filter(2:2:end,1:2:end, 3);
       reconstructed_image_2(1:2:end,1:2:end,3) = mosaic_rb_br_filter(1:2:end,1:2:end, 3);
       mse = immse(im2double(original), reconstructed_image_1);
       figure; imshow(abs(reconstructed_image_1-im2double(original))); title("Absolute Errors (Cubic)"); 
       fprintf("Cubic mse difference %f\n", mse);

       mse = immse(im2double(original), reconstructed_image_2);
       figure; imshow(abs(reconstructed_image_2-im2double(original))); title("Absolute Errors (Interpolated)"); 
       fprintf("Interpolated mse difference %f\n", mse);
       figure; imshow(reconstructed_image_2); title("Interpolation filters");
    end
    function run_compress(QF)
        original = imread("lena.tiff");
        Q = [16, 11, 10, 16, 24, 40, 51, 61;
            12, 12, 14, 19, 26, 58, 60, 55;
            14, 13, 16, 24, 40, 57, 69, 56;
            14, 17, 22, 29, 51, 87, 80, 62;
            18, 22, 37, 56, 68, 109, 103, 73;
            24, 35, 55, 64, 81, 104, 113, 92;
            49, 64, 78, 87, 103, 121, 120, 101;
            72, 92, 95, 98, 112, 100, 103, 99];
        if QF ~= 0
            if QF > 50
                k = (100-QF)/50;
            else
                k = 50/QF;
            end
            Q = min(255,k*Q);
        end
        % DCT
        fun = @(block_struct) dct2(block_struct.data);
        J = blockproc(original,[8,8],fun);

        
        % Quantization
        %fun = @(X) round(X.data./Q).*Q;    % to see the compressed image
        fun = @(X) round(X.data./Q);      % to save the quantization index
        Jq = blockproc(J,[8,8],fun);
        
        blockSize = 8;
        numBlocks = size(Jq, 1) / blockSize;
        quantizedMatrix = zeros(numBlocks, numBlocks, blockSize^2);
        for i = 1:numBlocks
            for j = 1:numBlocks
                quantizedMatrix(i, j, :) = reshape(Jq((i-1)*blockSize+1:i*blockSize, (j-1)*blockSize+1:j*blockSize), [1 1 blockSize^2]);
            end
        end
        imwrite(abs(Jq),sprintf('comp_%d.tiff',QF));
        % IDCT

        fun = @(X) round(X.data./Q).*Q; %  to see the compressed image
        Jq = blockproc(J,[8,8],fun);
        fun = @(block_struct) idct2(block_struct.data);
        compressed = blockproc(Jq,[8,8],fun);
        mse = immse(im2double(original), im2double(uint8(compressed)));
        disp(mse);
        if QF == 0
            figure; imshow(original); title("Original");
            figure; imshow(uint8(compressed)); title("Compressed");
            figure; imshow(abs(im2double(uint8(compressed))-im2double(original))); title("Errors");
        end
    end

    function run_blockwise()
        % Load the signal
        x = load("signal.mat").x;
        % Display the signal
        figure;
        imshow(x);
        title('Signal');
        % Define block size and FFT size
        blockSize = 128;
        fftSize = blockSize;
        
        % Reshape the signal into non-overlapping blocks
        xBlocks = reshape(x, blockSize, []);
        
        % Compute the 2D FFT of each block
        XBlocks = fftshift(fft2(reshape(xBlocks, blockSize, blockSize, []), fftSize, fftSize));
        
        % Compute the magnitude response of each block
        magXBlocks = abs(XBlocks);
        
        % Plot the magnitude responses using mesh
        for i = [1, 8, 16, 64, 256]
            figure;
            mesh(magXBlocks(:, :, i));
            if i == 64 || i == 256 
                title(sprintf('Block (%d, %d)', uint8(sqrt(i)), uint8(sqrt(i))));
            else
                title(sprintf('Block (%d, %d)', 1, i));
            end
        end
    end
    
    function run_filter(boundary)
        b = [ones(32,32),zeros(32,32);zeros(32,32), ones(32,32)];
        b = [b,b;b,b];
        figure; imshow(b); title("Original");
        b = im2double(b);
        h = ones(5,5);
        [img_rows, img_columns, ~] = size(b);
        [h_rows, h_columns] = size(h);

        filtered_img = zeros(img_rows, img_columns);
        
        for i = 1:img_rows
            for j = 1:img_columns
                response = 0;
                for k = 1:h_rows
                    for l = 1:h_columns
                        row_index = ceil(i - h_rows/2 + k - 1);
                        column_index = ceil(j - h_columns/2 + l - 1);
                        switch boundary
                            case 'zero'
                                if row_index < 1 || row_index > img_rows || column_index < 1 || column_index > img_columns
                                    value = 0;
                                else
                                    value = b(row_index, column_index);
                                end
                            case 'repeated'
                                if row_index < 1
                                    row_index = 1;
                                elseif row_index > img_rows
                                    row_index = img_rows;
                                end
                                if column_index < 1
                                    column_index = 1;
                                elseif column_index > img_columns
                                    column_index = img_columns;
                                end
                                value = b(row_index, column_index);
                            case 'periodic'
                                row_index = mod(row_index - 1, img_rows) + 1;
                                column_index = mod(column_index - 1, img_columns) + 1;
                                value = b(row_index, column_index);
                        end
                        % compute the filter response
                        response = response + h(k,l) * value;
                    end
                end
                % store the filtered value
                filtered_img(i,j) = response;
            end
        end
        % ground_truth = imfilter(img, h);
        % figure; imshow(ground_truth); title('Ground truth');
        figure; imshow(filtered_img); title(sprintf("Filtered image %s", boundary));
        figure; imshow(uint8(abs(b-filtered_img))); title(sprintf("Difference %s", boundary));
    end
plot_filters(2);
plot_filters(3);
run_scaler()
for boundary = ["zero", "repeated" "periodic"]
  run_filter(boundary);
end
run_demosaic();
run_compress(0);
for QF=10:10:90
    run_compress(QF);
end
MSE_scores = [9.1090e-04  5.0427e-04  3.7320e-04  3.0569e-04  2.6260e-04  2.2582e-04  1.8523e-04  1.3973e-04  8.2894e-05];
file_sizes = [28.3 35.6 41.6 47.1 52.3 58.1 67.1 82.2 108];
plot(MSE_scores, file_sizes);
xlabel("MSE scores");
ylabel("File size (KB)");
title("MSE vs File size");
run_blockwise();
% 
end