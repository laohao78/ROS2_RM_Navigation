// Copyright 2012 Open Source Robotics Foundation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Author: Ryan Shim

#include <ignition/math.hh>
#include <cmath>
#include <stdio.h>

#include <gazebo/common/common.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>


namespace gazebo
{
class Obstacle1: public ModelPlugin
{
public:
  void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
  {
    // Store the pointer to the model
    this->model = _parent;

    const ignition::math::Pose3d initial_pose = this->model->WorldPose();
    const ignition::math::Vector3d initial_pos = initial_pose.Pos();
    const ignition::math::Quaterniond initial_rot = initial_pose.Rot();

    // create the animation
    gazebo::common::PoseAnimationPtr anim(
      // name the animation "move_1",
      // make it last 260 seconds,
      // and set it on a repeat loop
      new gazebo::common::PoseAnimation("move1", 60.0, true));

    gazebo::common::PoseKeyFrame * key = nullptr;

    auto add_key_frame = [&](double time, double dx, double dy, double dz)
    {
      key = anim->CreateKeyFrame(time);
      key->Translation(initial_pos + ignition::math::Vector3d(dx, dy, dz));
      key->Rotation(initial_rot);
    };

    // Elliptical trajectory centered at initial position:
    // x = 1 * cos(theta), y = 2 * sin(theta)
    // Vertices: (+/-1, 0) and (0, +/-2)
    const double duration = 60.0;
    const int segments = 64;
    const double pi = 3.14159265358979323846;
    const double semi_axis_x = 1.0;
    const double semi_axis_y = 2.0;

    for (int i = 0; i <= segments; ++i)
    {
      const double ratio = static_cast<double>(i) / static_cast<double>(segments);
      const double theta = 2.0 * pi * ratio;
      const double time = duration * ratio;
      const double dx = semi_axis_x * std::cos(theta);
      const double dy = semi_axis_y * std::sin(theta);
      add_key_frame(time, dx, dy, 0.0);
    }

    // set the animation
    _parent->SetAnimation(anim);
  }

// Pointer to the model

private:
  physics::ModelPtr model;

// Pointer to the update event connection

private:
  event::ConnectionPtr updateConnection;
};
// Register this plugin with the simulator
GZ_REGISTER_MODEL_PLUGIN(Obstacle1)
}  // namespace gazebo
