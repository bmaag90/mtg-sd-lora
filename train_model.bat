accelerate launch diffusers\examples\text_to_image\train_text_to_image_lora.py ^
--pretrained_model_name_or_path="stabilityai/sd-turbo" ^
--dataset_name="data\datasets\card_name_5000" ^
--dataloader_num_workers=0 ^
--resolution=512 ^
--center_crop ^
--random_flip ^
--train_batch_size=1 ^
--gradient_accumulation_steps=4 ^
--max_train_steps=300 ^
--learning_rate=1e-04 ^
--max_grad_norm=1 ^
--lr_scheduler="cosine" ^
--lr_warmup_steps=0 ^
--output_dir="./models/model_cardname_5000" ^
--checkpointing_steps=50 ^
--validation_prompt="magic the gathering card artwork liliana" ^
--seed=1337 ^
--mixed_precision="fp16" ^
::--resume_from_checkpoint="latest"
