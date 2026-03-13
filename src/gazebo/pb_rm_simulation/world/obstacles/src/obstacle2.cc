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
#include <stdio.h>

#include <gazebo/common/common.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>

namespace gazebo
{
  class Obstacle2 : public ModelPlugin
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
          // name the animation "move_2",
          // make it last 260 seconds,
          // and set it on a repeat loop
          new gazebo::common::PoseAnimation("move2", 140.0, true));

      gazebo::common::PoseKeyFrame *key = nullptr;

      auto add_key_frame = [&](double time, double dx)
      {
        key = anim->CreateKeyFrame(time);
        key->Translation(initial_pos + ignition::math::Vector3d(dx, 0.0, 0.0));
        key->Rotation(initial_rot);
      };

      // Oscillate around initial position along x axis: offset in [-2, 2]
      add_key_frame(0.0, -2.0);
      add_key_frame(35.0, 2.0);
      add_key_frame(70.0, -2.0);
      add_key_frame(105.0, 2.0);
      add_key_frame(140.0, -2.0);

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
  GZ_REGISTER_MODEL_PLUGIN(Obstacle2)
} // namespace gazebo
