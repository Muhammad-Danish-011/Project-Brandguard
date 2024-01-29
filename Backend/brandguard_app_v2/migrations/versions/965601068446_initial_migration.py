"""Initial migration

Revision ID: 965601068446
Revises: 
Create Date: 2024-01-29 10:29:22.712165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '965601068446'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaigns',
    sa.Column('CampaignID', sa.Integer(), nullable=False),
    sa.Column('CampaignName', sa.String(), nullable=True),
    sa.Column('StartDate', sa.DateTime(), nullable=True),
    sa.Column('EndDate', sa.DateTime(), nullable=True),
    sa.Column('IntervalTime', sa.Integer(), nullable=True),
    sa.Column('Status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('CampaignID')
    )
    op.create_table('urls',
    sa.Column('URL_id', sa.Integer(), nullable=False),
    sa.Column('webpage_url', sa.String(), nullable=True),
    sa.Column('template_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('URL_id')
    )
    op.create_table('images',
    sa.Column('ImageID', sa.Integer(), nullable=False),
    sa.Column('CampaignID', sa.Integer(), nullable=True),
    sa.Column('Extension', sa.String(), nullable=True),
    sa.Column('ImagePath', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['CampaignID'], ['campaigns.CampaignID'], ),
    sa.PrimaryKeyConstraint('ImageID')
    )
    op.create_table('visibility',
    sa.Column('VisibilityID', sa.Integer(), nullable=False),
    sa.Column('CampaignID', sa.Integer(), nullable=True),
    sa.Column('DateTime', sa.DateTime(), nullable=True),
    sa.Column('Found_Status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['CampaignID'], ['campaigns.CampaignID'], ),
    sa.PrimaryKeyConstraint('VisibilityID')
    )
    op.create_table('websites',
    sa.Column('WebsiteID', sa.Integer(), nullable=False),
    sa.Column('CampaignID', sa.Integer(), nullable=True),
    sa.Column('WebsiteURL', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['CampaignID'], ['campaigns.CampaignID'], ),
    sa.PrimaryKeyConstraint('WebsiteID')
    )
    op.create_table('screenshots',
    sa.Column('ScreenshotID', sa.Integer(), nullable=False),
    sa.Column('CampaignID', sa.Integer(), nullable=True),
    sa.Column('WebsiteID', sa.Integer(), nullable=True),
    sa.Column('ImageID', sa.Integer(), nullable=True),
    sa.Column('Extension', sa.String(), nullable=True),
    sa.Column('Timestamp', sa.String(), nullable=True),
    sa.Column('FilePath', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['CampaignID'], ['campaigns.CampaignID'], ),
    sa.ForeignKeyConstraint(['ImageID'], ['images.ImageID'], ),
    sa.ForeignKeyConstraint(['WebsiteID'], ['websites.WebsiteID'], ),
    sa.PrimaryKeyConstraint('ScreenshotID')
    )
    op.create_table('ad_positions',
    sa.Column('AdPositionID', sa.Integer(), nullable=False),
    sa.Column('ScreenshotID', sa.Integer(), nullable=True),
    sa.Column('XCoordinate', sa.Float(), nullable=True),
    sa.Column('YCoordinate', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['ScreenshotID'], ['screenshots.ScreenshotID'], ),
    sa.PrimaryKeyConstraint('AdPositionID')
    )
    op.create_table('scraped_images',
    sa.Column('ScrapedImageID', sa.Integer(), nullable=False),
    sa.Column('ScreenshotID', sa.Integer(), nullable=True),
    sa.Column('Extension', sa.String(), nullable=True),
    sa.Column('FilePath', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['ScreenshotID'], ['screenshots.ScreenshotID'], ),
    sa.PrimaryKeyConstraint('ScrapedImageID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scraped_images')
    op.drop_table('ad_positions')
    op.drop_table('screenshots')
    op.drop_table('websites')
    op.drop_table('visibility')
    op.drop_table('images')
    op.drop_table('urls')
    op.drop_table('campaigns')
    # ### end Alembic commands ###
