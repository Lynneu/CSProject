<template>
  <q-page class="column">
    <q-list class="bg-white q-pa-md" separator style="padding-top: 66px">
      <q-item
        v-for="(task, index) in tasks"
        :key="task.title"
        @click="task.done = !task.done"
        :class="{ 'done bg-blue-1': task.done }"
        clickable
        v-ripple
      >
        <q-item-section avatar>
          <q-checkbox
            v-model="task.done"
            class="no-pointer-events"
            color="primary"
          />
        </q-item-section>
        <q-item-section>
          <q-item-label>{{ task.title }}</q-item-label>
        </q-item-section>
        <q-item-section v-if="task.done" side>
          <q-btn
            @click.stop="deleteTask(index)"
            flat
            round
            dense
            color="primary"
            icon="delete"
          />
        </q-item-section>
      </q-item>
    </q-list>
    <div v-if="!tasks.length" class="no-tasks absolute-center">
      <q-icon name="check" size="80px" color="primary" />
      <div class="text-h6 text-primary text-center">没有任务</div>
    </div>
    <div class="row">
      <q-page-sticky position="top-right" :offset="[18, 18]">
        <q-input
          bg-color="grey-2"
          filled
          bottom-slots
          clearable
          clear-icon="close"
          v-model="newTask"
          @keyup.enter="addTask"
          dense
          placeholder="添加待办事项"
        >
          <template v-slot:prepend>
            <q-icon name="event" color="primary" />
          </template>
          <template v-slot:append>
            <q-btn @click="addTask" round dense flat icon="add" />
          </template>
        </q-input>
      </q-page-sticky>
    </div>
  </q-page>
</template>

<script lang="ts">
export default {
  data() {
    return {
      color: [],
      newTask: '',
      tasks: [
        {
          title: 'Linux内存管理',
          done: false,
        },
        {
          title: '计控实验',
          done: false,
        },
        {
          title: '计算机系统结构实验',
          done: false,
        },
        {
          title: '汽车文化作业',
          done: false,
        },
        {
          title: '六级听力',
          done: false,
        },
        {
          title: '党校考试',
          done: false,
        },
        {
          title: '计控实验',
          done: false,
        },
        {
          title: '算法作业背包问题',
          done: true,
        },
        {
          title: '数据结构课设报告提交',
          done: true,
        },
      ],
    };
  },
  methods: {
    deleteTask(index: number) {
      this.$q
        .dialog({
          title: '确认',
          message: '是否确认删除?',
          cancel: '取消',
          persistent: true,
          ok: '是',
        })
        .onOk(() => {
          this.tasks.splice(index, 1);
          this.$q.notify('任务删除');
        });
    },
    addTask() {
      this.tasks.push({ title: this.newTask, done: false });
      this.newTask = '';
    },
  },
};
</script>

<style lang="scss">
.done {
  .q-item__label {
    text-decoration: line-through;
    color: #bbb;
  }
}
.no-tasks {
  opacity: 0.5;
}
.TodoHead {
  color: #3d72a6;
  background-color: #ffffff;
}
</style>
