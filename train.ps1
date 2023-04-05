# LoRA train script by @Akegarasu

# Train data path | Set training model and images
$pretrained_model = "./sd-models/v1-5-pruned.safetensors" # base model path
$train_data_dir = "./train/lrao" # train dataset path 
$reg_data_dir = "" # directory for regularization images, default is not to use regularization images.

# Network settings 
$network_module = "networks.lora" # # Set the type of network to be trained, default is networks.lora, which is LoRA training. If you want to train LyCORIS (LoCon, LoHa), change this value to lycoris.kohya
$network_weights = "" # pretrained weights for LoRA network, fill in the LoRA model path if you want to continue training from an existing LoRA model.
$network_dim = 128 # network dim, usually 4~128, not the bigger the better
$network_alpha = 64 # network alpha , usually the same value as network_dim or a smaller value, such as half of network_dim to prevent underflow. Default value is 1, using a smaller alpha requires increasing the learning rate.

# Train related params
$resolution = "512,512" # image resolution w,h. Supports non-square, but must be a multiple of 64.
$batch_size = 1 # batch size
$max_train_epoches = 6 # max train epoches
$save_every_n_epochs = 6 # save every n epochs

$train_unet_only = 0 # train U-Net only, turning this on will sacrifice performance and significantly reduce memory usage. 6G memory can be turned on
$train_text_encoder_only = 0 # train Text Encoder only 

$noise_offset = 0.1 # noise offset  noise offset, add noise offset during training to improve generation of very dark or very bright images, recommended parameter is 0.1 if enabled
$keep_tokens = 0 # keep heading N tokens when shuffling caption tokens 。

# Learning rate | 
$lr = "1e-4"
$unet_lr = "1e-4"
$text_encoder_lr = "1e-5"
$lr_scheduler = "cosine_with_restarts" # "linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"
$lr_warmup_steps = 0 # warmup steps, only need to fill in this value when lr_scheduler is constant_with_warmup
$lr_restart_cycles = 1 # cosine_with_restarts restart cycles, only effective when lr_scheduler is cosine_with_restarts.

# Output settings
$output_name = "lrao6" # output model name |
$save_model_as = "safetensors" # model save format: ckpt, pt, safetensors

# Other settings
$min_bucket_reso = 256 # arb min resolution
$max_bucket_reso = 1024 # arb max resolution
$persistent_data_loader_workers = 0 # persistent dataloader workers, easy to explode memory, keep loading training set worker, reduce pause between each epoch
$clip_skip = 2 #  clip skip, generally use 2

# Optimizer settings
$use_8bit_adam = 1 # use 8bit adam optimizer, save memory by default. Some old 10-series graphics cards cannot be used
$use_lion = 0 # use lion optimizer

# LyCORIS training settings
$algo = "lora" # LyCORIS network algo | LyCORIS network algorithm options are lora, loha. lora is also known as locon
$conv_dim = 4 # conv dim | Similar to network_dim, recommended to be 4
$conv_alpha = 4 # conv alpha | Similar to network_alpha, can use the same or smaller value as conv_dim

# ============= DO NOT MODIFY CONTENTS BELOW  =====================
# Activate python venv
.\venv\Scripts\activate

$Env:HF_HOME = "huggingface"
$ext_args = [System.Collections.ArrayList]::new()

if ($train_unet_only) {
  [void]$ext_args.Add("--network_train_unet_only")
}

if ($train_text_encoder_only) {
  [void]$ext_args.Add("--network_train_text_encoder_only")
}

if ($network_weights) {
  [void]$ext_args.Add("--network_weights=" + $network_weights)
}

if ($reg_data_dir) {
  [void]$ext_args.Add("--reg_data_dir=" + $reg_data_dir)
}

if ($use_8bit_adam) {
  [void]$ext_args.Add("--use_8bit_adam")
}

if ($use_lion) {
  [void]$ext_args.Add("--use_lion_optimizer")
}

if ($persistent_data_loader_workers) {
  [void]$ext_args.Add("--persistent_data_loader_workers")
}

if ($network_module -eq "lycoris.kohya") {
  [void]$ext_args.Add("--network_args")
  [void]$ext_args.Add("conv_dim=$conv_dim")
  [void]$ext_args.Add("conv_alpha=$conv_alpha")
  [void]$ext_args.Add("algo=$algo")
}

if ($noise_offset) {
  [void]$ext_args.Add("--noise_offset=$noise_offset")
}

# run train
accelerate launch --num_cpu_threads_per_process=8 "./sd-scripts/train_network.py" `
  --enable_bucket `
  --pretrained_model_name_or_path=$pretrained_model `
  --train_data_dir=$train_data_dir `
  --output_dir="./output" `
  --logging_dir="./logs" `
  --log_prefix=$output_name `
  --resolution=$resolution `
  --network_module=$network_module `
  --max_train_epochs=$max_train_epoches `
  --learning_rate=$lr `
  --unet_lr=$unet_lr `
  --text_encoder_lr=$text_encoder_lr `
  --lr_scheduler=$lr_scheduler `
  --lr_warmup_steps=$lr_warmup_steps `
  --lr_scheduler_num_cycles=$lr_restart_cycles `
  --network_dim=$network_dim `
  --network_alpha=$network_alpha `
  --output_name=$output_name `
  --train_batch_size=$batch_size `
  --save_every_n_epochs=$save_every_n_epochs `
  --mixed_precision="fp16" `
  --save_precision="fp16" `
  --seed="1337" `
  --cache_latents `
  --clip_skip=$clip_skip `
  --prior_loss_weight=1 `
  --max_token_length=225 `
  --caption_extension=".txt" `
  --save_model_as=$save_model_as `
  --min_bucket_reso=$min_bucket_reso `
  --max_bucket_reso=$max_bucket_reso `
  --keep_tokens=$keep_tokens `
  --xformers --shuffle_caption $ext_args
Write-Output "Train finished"
Read-Host | Out-Null ;