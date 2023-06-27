function m20225571_p1()
close all;
    function step_1_6(for_loop, integer_precision)
        img = imread("ColorChecker.jpeg");
        figure; imshow(img); title("Original Image"); 
        non_srgb_img = imread("ColorChecker.jpeg");
        disp(max(non_srgb_img(:)));
        disp(min(non_srgb_img(:)));
        non_srgb_img = double(non_srgb_img);
        non_srgb_img = non_srgb_img/255.0;
        if for_loop == true
            [M, N, C] = size(non_srgb_img);
            lin_srgb_img = zeros(M, N, C);
            for j = 1:M
                for k = 1: N
                    lin_srgb_img(j, k, 1) = non_srgb_img(j, k, 1).^2.2;
                    lin_srgb_img(j, k, 2) = non_srgb_img(j, k, 2).^2.2;
                    lin_srgb_img(j, k, 3) = non_srgb_img(j, k, 3).^2.2;
                end
            end
            figure; imshow(lin_srgb_img); title("Linear sRGB");
            lin_p3_rgb_img = zeros(M, N, C);
            for j = 1:M
                for k = 1: N
                    lin_p3_rgb_img(j, k, 1) = 0.8225 * lin_srgb_img(j, k, 1) + 0.1775 * lin_srgb_img(j, k, 2) + 0.0001 * lin_srgb_img(j, k, 3); 
                    lin_p3_rgb_img(j, k, 2) = 0.0331 * lin_srgb_img(j, k, 1) + 0.9668 * lin_srgb_img(j, k, 2) + 0.0000 * lin_srgb_img(j, k, 3);
                    lin_p3_rgb_img(j, k, 3) = 0.0171 * lin_srgb_img(j, k, 1) + 0.0724 * lin_srgb_img(j, k, 2) + 0.9105 * lin_srgb_img(j, k, 3);
                end
            end
            non_p3_rgb_img = zeros(M, N, C);
            for j = 1:M
                for k = 1: N
                    non_p3_rgb_img(j, k, 1) = lin_p3_rgb_img(j, k, 1).^(1/2.2);
                    non_p3_rgb_img(j, k, 2) = lin_p3_rgb_img(j, k, 2).^(1/2.2);
                    non_p3_rgb_img(j, k, 3) = lin_p3_rgb_img(j, k, 3).^(1/2.2);
                end
            end
            figure; imshow(non_p3_rgb_img); title("Nonlinear p3 RGB");
            figure; imshow(non_p3_rgb_img - non_srgb_img); title("p3 RGB - sRGB");
            xyz_srgb = zeros(M, N, C);
            xyz_p3_rgb = zeros(M, N, C);
            for j = 1:M
                for k = 1: N
                    xyz_srgb(j, k, 1) = 0.4124 * lin_srgb_img(j, k, 1) + 0.3576 * lin_srgb_img(j, k, 2) + 0.1805 * lin_srgb_img(j, k, 3); 
                    xyz_srgb(j, k, 2) = 0.2126 * lin_srgb_img(j, k, 1) + 0.7152 * lin_srgb_img(j, k, 2) + 0.0722 * lin_srgb_img(j, k, 3);
                    xyz_srgb(j, k, 3) = 0.0193 * lin_srgb_img(j, k, 1) + 0.1192 * lin_srgb_img(j, k, 2) + 0.9505 * lin_srgb_img(j, k, 3);
                    xyz_p3_rgb(j, k, 1) = 0.4866 * lin_p3_rgb_img(j, k, 1) + 0.2657 * lin_p3_rgb_img(j, k, 2) + 0.1982 * lin_p3_rgb_img(j, k, 3); 
                    xyz_p3_rgb(j, k, 2) = 0.2290 * lin_p3_rgb_img(j, k, 1) + 0.6917 * lin_p3_rgb_img(j, k, 2) + 0.0793 * lin_p3_rgb_img(j, k, 3);
                    xyz_p3_rgb(j, k, 3) = 0.0000 * lin_p3_rgb_img(j, k, 1) + 0.0451 * lin_p3_rgb_img(j, k, 2) + 1.0439 * lin_p3_rgb_img(j, k, 3);
                end
            end
            lab_srgb = xyz2lab(xyz_srgb);
            lab_p3_rgb = xyz2lab(xyz_p3_rgb);
            deltaE = sqrt((lab_srgb(:, :, 1) - lab_p3_rgb(:, :, 1)).^2 + (lab_srgb(:, :, 2) - lab_p3_rgb(:, :, 2)).^2 + (lab_srgb(:, :, 3) - lab_p3_rgb(:, :, 3)).^2);
            disp(mean(deltaE(:)));
            disp(max(deltaE(:)));
        else
            lin_srgb_img = non_srgb_img.^2.2;
            if integer_precision~=0
                lin_srgb_img = 2.^integer_precision.*lin_srgb_img;
                lin_srgb_img = round(lin_srgb_img);
            end
            figure; imshow(lin_srgb_img ./ 2.^integer_precision); title("Linear sRGB");
            p3_matrix = [0.8225 0.1775 0.0001; 0.0331 0.9668 0.0000; 0.0171 0.0724 0.9105];
            if integer_precision~=0
                p3_matrix = 2.^integer_precision.* p3_matrix;
                p3_matrix = round(p3_matrix);
            end
            xyz_srgb_matrix = [0.4124 0.3576 0.1805; 0.2126 0.7152 0.0722; 0.0193 0.1192 0.9505];
            xyz_p3_matrix = [0.4866 0.2657 0.1982; 0.2290 0.6917 0.0793; 0.0000 0.0451 1.0439];
            lin_srgb_img_2d = reshape(lin_srgb_img, [], 3);
            lin_p3_rgb_img_2d = lin_srgb_img_2d * p3_matrix';
            if integer_precision~=0
                lin_p3_rgb_img_2d = lin_p3_rgb_img_2d./2.^integer_precision;
                lin_p3_rgb_img_2d = round(lin_p3_rgb_img_2d);
                lin_p3_rgb_img_2d = lin_p3_rgb_img_2d./2.^integer_precision;
                lin_srgb_img_2d = lin_srgb_img_2d./2.^integer_precision;
            end
            lin_p3_rgb_img = reshape(lin_p3_rgb_img_2d, size(lin_srgb_img));
            non_p3_rgb_img = lin_p3_rgb_img.^(1/2.2);
            figure; imshow(non_p3_rgb_img); title("Nonlinear p3 RGB");
            figure; imshow(non_p3_rgb_img - non_srgb_img); title("p3 RGB - sRGB");
            lin_p3_rgb_img_2d = reshape(lin_p3_rgb_img, [], 3);
            xyz_srgb = lin_srgb_img_2d * xyz_srgb_matrix';
            xyz_p3_rgb = lin_p3_rgb_img_2d * xyz_p3_matrix';
            xyz_srgb = reshape(xyz_srgb, size(lin_srgb_img));
            xyz_p3_rgb = reshape(xyz_p3_rgb, size(lin_srgb_img));
            lab_srgb = xyz2lab(xyz_srgb);
            lab_p3_rgb = xyz2lab(xyz_p3_rgb);
            deltaE = sqrt((lab_srgb(:, :, 1) - lab_p3_rgb(:, :, 1)).^2 + (lab_srgb(:, :, 2) - lab_p3_rgb(:, :, 2)).^2 + (lab_srgb(:, :, 3) - lab_p3_rgb(:, :, 3)).^2);
            disp(mean(deltaE(:)));
            disp(max(deltaE(:)));
            
        end
    end
    step_1_6(false, 0);
end