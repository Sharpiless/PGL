#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import os
import time
import argparse

from utils.args import ArgumentGroup

# yapf: disable
parser = argparse.ArgumentParser(__doc__)
parser.add_argument('--use_cuda', action='store_true')
model_g = ArgumentGroup(parser, "model", "model configuration and paths.")
model_g.add_arg("init_checkpoint",          str,  None,           "Init checkpoint to resume training from.")
model_g.add_arg("init_pretraining_params",  str,  None,
                "Init pre-training params which preforms fine-tuning from. If the "
                 "arg 'init_checkpoint' has been set, this argument wouldn't be valid.")
model_g.add_arg("./save_dir",              str,  "./checkpoints",  "Path to save checkpoints.")
model_g.add_arg("hidden_size",             int,    128,       "hidden size.")


train_g = ArgumentGroup(parser, "training", "training options.")
train_g.add_arg("epoch",             int,    3,       "Number of epoches for fine-tuning.")
train_g.add_arg("learning_rate",     float,  5e-5,    "Learning rate used to train with warmup.")
train_g.add_arg("lr_scheduler",      str,    "linear_warmup_decay",
                "scheduler of learning rate.", choices=['linear_warmup_decay', 'noam_decay'])
train_g.add_arg("weight_decay",      float,  0.01,    "Weight decay rate for L2 regularizer.")
train_g.add_arg("warmup_proportion", float,  0.1,
                "Proportion of training steps to perform linear learning rate warmup for.")
train_g.add_arg("save_steps",        int,    10000,   "The steps interval to save checkpoints.")
train_g.add_arg("validation_steps",  int,    1000,    "The steps interval to evaluate model performance.")
train_g.add_arg("use_dynamic_loss_scaling",    bool,   True,   "Whether to use dynamic loss scaling.")
train_g.add_arg("init_loss_scaling",           float,  102400,
                "Loss scaling factor for mixed precision training, only valid when use_fp16 is enabled.")

train_g.add_arg("test_save",            str,    "./checkpoints/test_result",       "test_save")
train_g.add_arg("metric",               str,    "simple_accuracy",   "metric")
train_g.add_arg("incr_every_n_steps",          int,    100,   "Increases loss scaling every n consecutive.")
train_g.add_arg("decr_every_n_nan_or_inf",     int,    2,
                "Decreases loss scaling every n accumulated steps with nan or inf gradients.")
train_g.add_arg("incr_ratio",                  float,  2.0,
                "The multiplier to use when increasing the loss scaling.")
train_g.add_arg("decr_ratio",                  float,  0.8,
                "The less-than-one-multiplier to use when decreasing.")




log_g = ArgumentGroup(parser,     "logging", "logging related.")
log_g.add_arg("skip_steps",          int,    10,    "The steps interval to print loss.")
log_g.add_arg("verbose",             bool,   False, "Whether to output verbose log.")
log_g.add_arg("log_dir",             str,   './logs/', "Whether to output verbose log.")

data_g = ArgumentGroup(parser, "data", "Data paths, vocab paths and data processing options")
data_g.add_arg("tokenizer",           str, "FullTokenizer",
              "ATTENTION: the INPUT must be splited by Word with blank while using SentencepieceTokenizer or WordsegTokenizer")
data_g.add_arg("train_set",           str,  None,  "Path to training data.")
data_g.add_arg("test_set",            str,  None,  "Path to test data.")
data_g.add_arg("dev_set",             str,  None,  "Path to validation data.")
data_g.add_arg("aug1_type",           str,  "scheme1",  "augment type")
data_g.add_arg("aug2_type",           str,  "scheme1",  "augment type")
data_g.add_arg("batch_size",          int,  32,    "Total examples' number in batch for training. see also --in_tokens.")
data_g.add_arg("predict_batch_size",  int,  None,    "Total examples' number in batch for predict. see also --in_tokens.")
data_g.add_arg("random_seed",         int,  None,     "Random seed.")
data_g.add_arg("buf_size",         int,  1000,     "Random seed.")

run_type_g = ArgumentGroup(parser, "run_type", "running type options.")
run_type_g.add_arg("num_iteration_per_drop_scope", int,    10,    "Iteration intervals to drop scope.")
run_type_g.add_arg("do_train",                     bool,   True,  "Whether to perform training.")
run_type_g.add_arg("do_val",                       bool,   True,  "Whether to perform evaluation on dev data set.")
run_type_g.add_arg("do_test",                      bool,   True,  "Whether to perform evaluation on test data set.")
run_type_g.add_arg("metrics",                      bool,   True,  "Whether to perform evaluation on test data set.")
run_type_g.add_arg("shuffle",                      bool,   True,  "")
run_type_g.add_arg("for_cn",                       bool,   True,  "model train for cn or for other langs.")
run_type_g.add_arg("num_workers",                       int,   1,  "use multiprocess to generate graph")
run_type_g.add_arg("output_dir",                       str,   None,  "path to save model")
run_type_g.add_arg("config",                       str,   None,  "configure yaml file")
run_type_g.add_arg("n",                       str,   None,  "task name")
run_type_g.add_arg("task_name", str,   None,  "task name")
run_type_g.add_arg("pretrain", bool,   False,  "Whether do pretrian")
run_type_g.add_arg("pretrain_name", str,   None,  "pretrain task name")
run_type_g.add_arg("pretrain_config", str,   None,  "pretrain config.yaml file")
run_type_g.add_arg("pretrain_model_step", str,   None,  "pretrain model step")
run_type_g.add_arg("model_type", str,   "BaseLineModel",  "pretrain model step")
run_type_g.add_arg("num_class", int,   1,  "number class")
run_type_g.add_arg("dataset_name", str,   None,  "finetune dataset name")
run_type_g.add_arg("eval_metrics", str,   None,  "evaluate metrics")
run_type_g.add_arg("task_type", str,   None,  "regression or classification")
