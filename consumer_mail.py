import yagmail
import json
import os
import sys

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def create_subject(status):
    return '[Hawthorn]: 任务状态 <{status}> 勿回'.format(status=status)


def render_template(template, **kwargs):
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()

    import jinja2
    template_loader = jinja2.FileSystemLoader(searchpath="/")
    template_env = jinja2.Environment(loader=template_loader,
                                      trim_blocks=True,
                                      lstrip_blocks=True, )
    template_engine = template_env.get_template(template)
    return template_engine.render(**kwargs)


def callback(ch, method, properties, body):
    yag = yagmail.SMTP(user='monitor-fe@jiedaibao.com',
                       password='L8n2@A#reT3mN54YQfe',
                       host='smtp.exmail.qq.com',
                       port=587,
                       smtp_ssl=False)
    data = json.loads(body)
    # exchange_name = method.exchange
    if 'mail' in data and data['mail']:
        # TODO format content
        yag.send(to=data['mail'],
                 subject=create_subject(data['status']),
                 contents=[
                     '',
                     render_template(os.path.join(ROOT_DIR, 'mail.html'), data=data).replace('\n', ' ')
                 ])
    ch.basic_ack(delivery_tag=method.delivery_tag)
