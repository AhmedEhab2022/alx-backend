import createPushNotificationsJobs from "./8-job";
import kue from "kue";

const queue = kue.createQueue();

describe("createPushNotificationsJobs", function () {
  before(function () {
    queue.testMode.enter();
  });

  afterEach(function () {
    queue.testMode.clear();
  });

  after(function () {
    queue.testMode.exit();
  });

  it("createPushNotificationsJobs", function () {
    createPushNotificationsJobs(
      [
        {
          phoneNumber: "4153518780",
          message: "This is the code 1234 to verify your account",
        },
      ],
      queue
    );
    expect(queue.testMode.jobs.length).to.equal(1);
    expect(queue.testMode.jobs[0].type).to.equal("push_notification_code_2");
    expect(queue.testMode.jobs[0].data).to.eql({
      phoneNumber: "4153518780",
      message: "This is the code 1234 to verify your account",
    });
  });

  it("createPushNotificationsJobs", function () {
    createPushNotificationsJobs(
      [
        {
          phoneNumber: "4153518780",
          message: "This is the code 1234 to verify your account",
        },
        {
          phoneNumber: "4153518781",
          message: "This is the code 1234 to verify your account",
        },
      ],
      queue
    );
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].type).to.equal("push_notification_code_2");
    expect(queue.testMode.jobs[0].data).to.eql({
      phoneNumber: "4153518780",
      message: "This is the code 1234 to verify your account",
    });
    expect(queue.testMode.jobs[1].type).to.equal("push_notification_code_2");
    expect(queue.testMode.jobs[1].data).to.eql({
      phoneNumber: "4153518781",
      message: "This is the code 1234 to verify your account",
    });
  });

  it("createPushNotificationsJobs", function () {
    createPushNotificationsJobs([], queue);
    expect(queue.testMode.jobs.length).to.equal(0);
  });
});
