# Copyright 2018 The TensorFlow Authors All Rights Reserved.
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
# ==============================================================================

"""A script to define flags.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import os

# Shared flags.
tf.app.flags.DEFINE_enum("mode", "train",
                         ["train", "eval", "sample"],
                         "The mode of the binary.")
tf.app.flags.DEFINE_enum("model", "vrnn",
                         ["vrnn", "ghmm", "srnn"],
                         "Model choice.")
tf.app.flags.DEFINE_integer("latent_size", 216,
                            "The size of the latent state of the model.")
tf.app.flags.DEFINE_integer("num_layers", 3,
                            "Number of RNN layers.")
tf.app.flags.DEFINE_enum("dataset_type", "speech",
                         ["pianoroll", "speech", "pose"],
                         "The type of dataset.")
tf.app.flags.DEFINE_string("dataset_path", "./datasets/trainASF_3_54.tfrecord",
                           "Path to load the dataset from.")
tf.app.flags.DEFINE_integer("data_dimension", 54,
                            "The dimension of each vector in the data sequence. "
                            "Defaults to 88 for pianoroll datasets and 200 for speech "
                            "datasets. Should not need to be changed except for "
                            "testing.")
tf.app.flags.DEFINE_integer("sequence_length", 300,
                            "Sequence_length.")
tf.app.flags.DEFINE_integer("batch_size", 16,
                            "Batch size.")
tf.app.flags.DEFINE_integer("num_samples", 1,
                            "The number of samples (or particles) for multisample "
                            "algorithms.")
tf.app.flags.DEFINE_float("noise_std", 0.25,
                          "Noise std.")
tf.app.flags.DEFINE_float("keep_prob", 0.5,
                          "Keep probability.")
tf.app.flags.DEFINE_float("lambda_loss", 0.0015,
                          "Lambda loss amount.")
tf.app.flags.DEFINE_string("log_dir", "./chkpts",
                           "The directory to keep checkpoints and summaries in.")
tf.app.flags.DEFINE_integer("random_seed", None,
                            "A random seed for seeding the TensorFlow graph.")
tf.app.flags.DEFINE_integer("parallel_iterations", 30,
                            "The number of parallel iterations to use for the while "
                            "loop that computes the bounds.")

# Training flags.
tf.app.flags.DEFINE_enum("bound", "elbo",
                         ["elbo", "iwae", "fivo", "fivo-aux"],
                         "The bound to optimize.")

tf.app.flags.DEFINE_float("learning_rate", 0.0025,
                          "The learning rate for ADAM.")
tf.app.flags.DEFINE_integer("max_steps", int(1e9),
                            "The number of gradient update steps to train for.")
tf.app.flags.DEFINE_integer("summarize_every", 100,
                            "The number of steps between summaries.")


# Distributed training flags.
tf.app.flags.DEFINE_string("master", "",
                           "The BNS name of the TensorFlow master to use.")
tf.app.flags.DEFINE_integer("task", 0,
                            "Task id of the replica running the training.")
tf.app.flags.DEFINE_integer("ps_tasks", 0,
                            "Number of tasks in the ps job. If 0 no ps job is used.")
tf.app.flags.DEFINE_boolean("stagger_workers", True,
                            "If true, bring one worker online every 1000 steps.")

tf.app.flags.DEFINE_enum("proposal_type", "filtering",
                         ["prior", "filtering", "smoothing"],
                         "Unused")

# Evaluation flags.
tf.app.flags.DEFINE_enum("split", "train",
                         ["train", "test", "valid"],
                         "Split to evaluate the model on.")


# For Evaluation
tf.app.flags.DEFINE_boolean("plot", True,
                            "If true, plot the results ")
tf.app.flags.DEFINE_boolean("rerun_graph", True,
                            "If true, rerun the evaluation graph")
tf.app.flags.DEFINE_boolean("dump_result", True,
                            "If true, dump the result")
tf.app.flags.DEFINE_boolean("use_contrario", True,
                            "If true, use contrario ")
tf.app.flags.DEFINE_boolean("use_correction", True,
                            "If true, use prior knowledge to improve the detection ")
tf.app.flags.DEFINE_integer("anomaly_threshold", -500,
                            ".")
tf.app.flags.DEFINE_integer("peak_threshold", -700,
                            ".")
tf.app.flags.DEFINE_integer("percentile", 35,
                            ".")
tf.app.flags.DEFINE_integer("max_seq_len", 100,
                            ".")
tf.app.flags.DEFINE_integer("min_seg_len", 1,
                            ".")
tf.app.flags.DEFINE_integer("filter_size", 51,
                            ".")
tf.app.flags.DEFINE_float("contrario_eps", 3e-4,
                          ".")


# Solve tf >=1.8.0 flags bug
tf.app.flags.DEFINE_string('log_filename', '', 'log filename')
tf.app.flags.DEFINE_string('logdir', '', 'log directory')

FLAGS = tf.app.flags.FLAGS
config = FLAGS

# LOG DIR
config.log_filename = "lstm_dae"+"-"\
                      +"latent_size"+"-"+str(config.latent_size)+"-"\
                      +"noise_std" + "-"+str(config.noise_std)+"-"\
                      +os.path.basename(config.dataset_path)
config.logdir = os.path.join(config.log_dir,config.log_filename)
config.logdir = config.logdir.replace("test","train")
config.logdir = config.logdir.replace("valid","train")

if not os.path.exists(config.logdir):
    if config.mode == "train":
        os.mkdir(config.logdir)
    else:
        raise ValueError(config.logdir + " doesnt exist!")
