# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://aws.amazon.com/apache2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

"""Launch a lifecycle cloudwatch_logger node"""

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.actions import OpaqueFunction
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    node_name = LaunchConfiguration("node_name")
    config_file_path = LaunchConfiguration("config_file_path")

    if context.perform_substitution(config_file_path) == "":
        config_file_path = PathJoinSubstitution(
            [FindPackageShare("cloudwatch_logger"), "config", "sample.yaml"])

    node = Node(
        package="cloudwatch_logger",
        executable="cloudwatch_logger",
        name=node_name,
        parameters=[config_file_path],
        # workaround until https://github.com/ros2/rmw_fastrtps/issues/265 is resolved
        arguments=["__log_disable_rosout:=true"],
        output="screen",
    )

    output_log_actions = [LogInfo(msg=config_file_path)]
    return output_log_actions + [node]


def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "node_name",
            default_value="cloudwatch_logger",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "config_file_path",
            default_value="",
        )
    ) 

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
